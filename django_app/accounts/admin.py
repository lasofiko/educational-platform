from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','grade','target_score','created_at')
    search_fields = ('user__username','user__first_name','user__last_name','patronymic')
    list_filter = ('grade',)
    readonly_fields=('created_at','updated_at')


