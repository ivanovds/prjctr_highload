from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EntryViewSet, ElasticView

router = DefaultRouter()
router.register(r'entries', EntryViewSet, 'entry')

urlpatterns = [
    path('', include(router.urls)),

    path('elastic/', ElasticView.as_view())
]
