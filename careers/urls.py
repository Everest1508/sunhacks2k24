from django.urls import path, include
from rest_framework.routers import DefaultRouter
from careers.views import CareerViewSet,ApplicationAPIView

router = DefaultRouter()
router.register(r'jobs', CareerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('application/', ApplicationAPIView.as_view()),
]
