from .models import UserProfile


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def profile_payload(user):
    profile = get_or_create_profile(user)
    return {
        'role': profile.role,
        'role_display': profile.get_role_display(),
        'grade': profile.grade,
        'target_score': profile.target_score,
    }
