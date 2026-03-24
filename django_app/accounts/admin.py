from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_grade')

    def get_grade(self, obj):
        return obj.profile.grade if hasattr(obj, 'profile') else '-'

    get_grade.short_description = 'Класс'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "grade", "phone")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("grade",)