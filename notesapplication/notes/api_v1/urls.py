from django.urls import path
from rest_framework.routers import DefaultRouter
from notes.api_v1 import views
from .views import NotesViewSet

router = DefaultRouter()
router.register("", NotesViewSet, basename="Notes")
urlpatterns = [] + router.urls
