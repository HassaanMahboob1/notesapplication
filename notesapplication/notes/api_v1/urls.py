from django.urls import path
from rest_framework.routers import DefaultRouter
from notes.api_v1 import views
from .views import NotesViewSet, CommentViewSet

router = DefaultRouter()
router.register("notes", NotesViewSet, basename="Notes")
router.register("comments", CommentViewSet, basename="Comment")
urlpatterns = [] + router.urls
