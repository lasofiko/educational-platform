from django.contrib import admin
from .models import UserProgress,Enrollment

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user','node','status','score','created_at')
    list_filter = ('status',)
    readonly_fields = ('completed_at','created_at','updated_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=('user','subject','enrolled_at')
    list_filter = ('subject',)
    readonly_fields = ('enrolled_at',)