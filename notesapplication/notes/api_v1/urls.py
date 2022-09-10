from django.urls import path
from notes.api_v1 import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet
from .views import NotesViewSet

router = DefaultRouter()
router.register("notes", NotesViewSet, basename="Notes")
router.register("comments", CommentViewSet, basename="Comment")
urlpatterns = [] + router.urls
