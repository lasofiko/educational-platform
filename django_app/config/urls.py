from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/courses/", include("courses.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/progress/", include("progress.urls")),
]
