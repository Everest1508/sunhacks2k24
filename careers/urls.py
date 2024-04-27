from django.urls import path, include
from rest_framework.routers import DefaultRouter
from careers.views import CareerViewSet,ApplicationAPIView,upload_files,admin_view

router = DefaultRouter()
router.register(r'jobs', CareerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('application/', ApplicationAPIView.as_view()),
    path('admin-view/', admin_view),
    path('upload/', upload_files, name='upload_files'),
]
