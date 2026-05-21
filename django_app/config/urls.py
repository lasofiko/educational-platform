from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "service": "django"})


urlpatterns = [
    path("api/v1/health/", health),
    path("admin/", admin.site.urls),
    path("api/v1/courses/", include("courses.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/progress/", include("progress.urls")),
]
