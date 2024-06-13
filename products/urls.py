from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductListView, ProductDetailView, CategoryViewSet, ProductListCreateView, ProductRetrieveUpdateDeleteView

router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductListCreateView.as_view(), name='product-create'),
    path('products/update-delete/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-retrieve-update-delete'),
    path('', include(router.urls)),
]
