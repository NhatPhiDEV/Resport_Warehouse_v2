from django.urls import path,include
from rest_framework import routers
from apps.views import ReportsViewSet
router = routers.DefaultRouter()
router.register('reports',ReportsViewSet, 'reports')
urlpatterns = [
    path('',include(router.urls))
]