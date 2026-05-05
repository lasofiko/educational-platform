from django.db import transaction
from django.db.models import Prefetch
from django.core.cache import cache
from courses.models import RoadmapNode, Subject
from progress.models import UserProgress
from courses.exceptions import NodeLocked, NodeNotFound
from django.contrib.auth.models import User

class RoadmapService:
    """сервис для работы с деревом Roadmap и разблокировкой узлов"""
    unlock = 70
    @staticmethod
    def get_tree(subject_id, user=None):
        """получить всё дерево узлов для предмета с учетом прогресса пользователя"""
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise NodeNotFound(f"Предмет {subject_id} не найден")
        root_nodes = RoadmapNode.objects.filter(subject_id=subject_id,parent=None).prefetch_related(Prefetch('children', queryset=RoadmapNode.objects.select_related('parent')), Prefetch('children__children')).order_by('order')
        user_progress = {}
        if user and user.is_authenticated:
            progresses = UserProgress.objects.filter(user=user,node__subject_id=subject_id).select_related('node')
            user_progress = {p.node_id: p for p in progresses}
        def build_tree(node):
            node_data = {
                'id': node.id,
                'title': node.title,
                'description': node.description,
                'node_type': node.node_type,
                'order': node.order,
                'task_number': node.task_number,
                'parent_id': node.parent_id,
                'subject_id': node.subject_id,
                'status': node.status,
                'user_status': _get_user_status(node, user_progress),
                'children': []
            }
            children = node.children.all().order_by('order')
            for child in children:
                node_data['children'].append(build_tree(child))
            return node_data
        tree = []
        for node in root_nodes:
            tree.append(build_tree(node))
        return tree

    @staticmethod
    def get_node_with_status(node_id, user):
        """получить узел с текущим статусом для пользователя"""
        try:
            node = RoadmapNode.objects.get(id=node_id)
        except RoadmapNode.DoesNotExist:
            raise NodeNotFound(node_id)
        progress, created = UserProgress.objects.get_or_create(user=user,node=node,defaults={'status': 'locked'})

        if node.parent is None and node.order == 0 and progress.status == 'locked':
            if created or progress.status == 'locked':
                progress.status = 'unlocked'
                progress.save()
        if progress.status == 'locked':
            raise NodeLocked(node_id)
        result = {
            'id': node.id,
            'title': node.title,
            'description': node.description,
            'node_type': node.node_type,
            'order': node.order,
            'task_number': node.task_number,
            'parent_id': node.parent_id,
            'subject_id': node.subject_id,
            'status': node.status,
            'user_status': progress.status,
            'user_score': progress.score,
            'user_completed_at': progress.completed_at,
            'children': []
        }
        children = node.children.all().order_by('order')
        for child in children:
            child_progress, _ = UserProgress.objects.get_or_create(user=user,node=child,defaults={'status': 'locked'})
            result['children'].append({
                'id': child.id,
                'title': child.title,
                'node_type': child.node_type,
                'order': child.order,
                'user_status': child_progress.status,
            })

        return result

    @staticmethod
    @transaction.atomic
    def unlock_next_node(user, completed_node_id, score_percentage=None):
        """разблокировать следующий узел после завершения текущего"""
        #получаем завершенный узел
        try:
            completed_node = RoadmapNode.objects.get(id=completed_node_id)
        except RoadmapNode.DoesNotExist:
            raise NodeNotFound(completed_node_id)
        progress, created = UserProgress.objects.get_or_create(user=user,node=completed_node,defaults={'status': 'in_progress'})

        if score_percentage is not None and score_percentage < RoadmapService.unlock:
            progress.status = 'in_progress'
            progress.score = int(score_percentage)
            progress.save()
            return None
        progress.status = 'complete'
        progress.score = int(score_percentage) if score_percentage else 100
        from django.utils import timezone
        progress.completed_at = timezone.now()
        progress.save()
        unlocked_nodes = []
        siblings = RoadmapNode.objects.filter(parent=completed_node.parent).order_by('order')
        current_index = None
        for i, sibling in enumerate(siblings):
            if sibling.id == completed_node.id:
                current_index = i
                break

        if current_index is not None and current_index + 1 < len(siblings):
            next_node = siblings[current_index + 1]
            next_progress, _ = UserProgress.objects.get_or_create(user=user,node=next_node,defaults={'status': 'locked'})
            if next_progress.status == 'locked':
                next_progress.status = 'unlocked'
                next_progress.save()
                unlocked_nodes.append({
                    'id': next_node.id,
                    'title': next_node.title,
                    'status': 'unlocked'
                })
        if completed_node.parent:
            all_children_completed = RoadmapService._are_all_children_completed(user, completed_node.parent)
            if all_children_completed:
                parent_node = completed_node.parent
                parent_completed = RoadmapService._get_parent_completion_status(user, parent_node)
                if not parent_completed:
                    parent_progress, _ = UserProgress.objects.get_or_create(user=user,node=parent_node,defaults={'status': 'in_progress'})
                    parent_progress.status = 'complete'
                    parent_progress.save()
                    next_parent_unlock = RoadmapService.unlock_next_node(user, parent_node.id, 100)
                    if next_parent_unlock:
                        unlocked_nodes.extend([next_parent_unlock] if isinstance(next_parent_unlock, dict) else next_parent_unlock)
        if len(unlocked_nodes) == 1:
            return unlocked_nodes[0]
        elif len(unlocked_nodes) > 1:
            return unlocked_nodes
        return None

    @staticmethod
    def _are_all_children_completed(user, parent_node):
        """проверить, все ли дочерние узлы родителя завершены"""
        children = parent_node.children.all()
        if not children.exists():
            return False
        children_progress = UserProgress.objects.filter(user=user,node__in=children)
        children_status = {p.node_id: p.status for p in children_progress}
        for child in children:
            status = children_status.get(child.id, 'locked')
            if status != 'complete':
                return False
        return True

    @staticmethod
    def _get_parent_completion_status(user, parent_node):
        """получить статус завершения родительского узла"""
        try:
            progress = UserProgress.objects.get(user=user, node=parent_node)
            return progress.status == 'complete'
        except UserProgress.DoesNotExist:
            return False
def get_tree(subject_id, user=None):
    return RoadmapService.get_tree(subject_id, user)

def get_node_with_status(node_id, user):
    return RoadmapService.get_node_with_status(node_id, user)

def unlock_next_node(user, completed_node_id, score_percentage=None):
    return RoadmapService.unlock_next_node(user, completed_node_id, score_percentage)

def _get_user_status(node, user_progress):
    progress = user_progress.get(node.id)
    if progress:
        return progress.status
    return 'locked'