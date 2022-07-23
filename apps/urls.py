from django.urls import path,include
from rest_framework.routers import DefaultRouter
from apps.views import ReportsViewSet,GetDataViewSet
router = DefaultRouter()
router.register('reports',ReportsViewSet, basename = 'reports')
router.register('datasets',GetDataViewSet, basename = 'datasets')
urlpatterns = [
    path('',include(router.urls))
]