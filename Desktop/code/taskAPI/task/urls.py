from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MeView, TaskViewSet, HealthCheckView

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")


urlpatterns = [
    path("api/me/", MeView.as_view()),
    path("health/", HealthCheckView.as_view()),
] + router.urls