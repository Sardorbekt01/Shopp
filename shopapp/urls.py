from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('product', Productoption, basename='product')
router.register('category', Categoryoption, basename='category')
router.register('customer', Customeroption, basename='customer')
router.register('item',OrderItemoption, basename='item')
router.register('order',Orderoption, basename='order')
router.register('shopcard',Shopcardoption, basename='shopcard')
[]
urlpatterns = router.urls

urlpatterns = [
    path('orders/<int:pk>/',top_purchase, name='top_orders'),
    path('selling/',best_selling_products, name='Eng kop sotilayotgan mahsulotlar'),
    path('expired/', expired_products, name='Muddati otgan'),
    path('market_price/',total_market, name='market_price'),
    path('exsel/<int:customer_id>/', exsel, name='exsel format'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls