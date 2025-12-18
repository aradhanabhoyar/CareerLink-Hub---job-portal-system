from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobApplicationViewSet, RegisterView

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', JobApplicationViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),  
]

