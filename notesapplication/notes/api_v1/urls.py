from django.urls import path
from rest_framework.routers import DefaultRouter
from notes.api_v1 import views
from .views import NotesViewSet, ArchiveViewSet, shared

router = DefaultRouter()
router.register("", NotesViewSet, basename="Notes")
router.register("archive", ArchiveViewSet, basename="Notes")
urlpatterns = [
    path("share", views.shared, name="shared"),
] + router.urls
