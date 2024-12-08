from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, ClientDetailAPIView
from django.urls import path, include

# Initialize the router
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')

# Custom paths combined with router URLs
urlpatterns = [
    # path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),  # Custom detail API
    path('clients/<int:client_pk>/projects/', ProjectViewSet.as_view({'post': 'create'}), name='create_project'),
    path('', include(router.urls)),  # Include router-generated URLs
]
