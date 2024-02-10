from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import *
from .serializers import *
import openpyxl
import pandas as pd
import io
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token   
from django.db.models.functions import Coalesce
from django.db.models import F, Sum
from django.core.exceptions import ValidationError




class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        strtoken = request.headers ["Authorization"]
        user = Token.objects.get(key=strtoken [6:1]).user
        content ={'message': f'Hello, {user}!'}
        return Response(content)


class Customeroption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class Productoption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class Categoryoption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Orderoption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemoption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class Shopcardoption(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ShopCart.objects.all()
    serializer_class = ShopcardSerializer

@api_view(['GET'])
#Bu api marketdagi barcha maxsulotlarning umumiy summasini xisoblaydi
@permission_classes([IsAuthenticated])
def total_market(request):
    total_price = Product.objects.aggregate(total_price=models.Sum('price'))['total_price'] or 0
    response_data = {
        'total_products_price': total_price
    }
    return Response(response_data)


@api_view(['GET'])
# Bu Api muddati o'tgan tovarlarni olib keladi
@permission_classes([IsAuthenticated])
def expired_products(request):
    today = timezone.now()
    expired_products = Product.objects.filter(expiry_date__lte=today)
    expired_products_list = []
    for product in expired_products:
        recommended_sell_by = product.expiry_date - timezone.timedelta(days=7) 
        expired_products_list.append({
            'product_id': product.id,
            'product_name': product.name,
            'price': str(product.price),
            'quantity': product.quantity,
            'expiry_date': product.expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
            'recommended_sell_by': recommended_sell_by.strftime("%Y-%m-%d %H:%M:%S")
        })

    response_data = {
        'expired_products': expired_products_list
    }

    return Response(response_data)





@api_view(['GET'])
# Bu Api eng ko'p sotlayotgan maxsulotlarni olib keladi
@permission_classes([IsAuthenticated])
def best_selling_products(request):
    try:
        total_sold_for_products = OrderItem.objects.values('product_id').annotate(total_sold=Coalesce(Sum('mount'), 0))
        response_data = {
            'total_sold_for_products': total_sold_for_products,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except OrderItem.DoesNotExist:
        return Response({"detail": "Hozircha xaridlar mavjud emas"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
# Bu Api bir Customerning sotib olgan haridlarini olib keladi va exsel formatga yozadi
@permission_classes([IsAuthenticated])
def exsel(request, customer_id):
    try:
        customer_orders = OrderItem.objects.filter(order__customer_id=customer_id)
        serializer = OrderItemSerializer(customer_orders, many=True)

        data = serializer.data
        df = pd.DataFrame(data)

        excel_filename = f"customer_orders_{customer_id}.xlsx"
        df.to_excel(excel_filename, index=False)

        return Response({"detail": "Malumotlar Excel fayliga yozildi", "file_name": excel_filename},
                        status=status.HTTP_200_OK)

    except OrderItem.DoesNotExist:
        return Response({"detail": "Hozircha xaridlar mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
# Bu Api Customerning 1000000so'mdan ortiq harid qilganini tekshiradi
@permission_classes([IsAuthenticated])
def top_purchase(request, *args, **kwargs):
    customer = get_object_or_404(Customer,  id=kwargs['pk'])
    purchases = OrderItem.objects.filter(order__customer=customer)

    total_quantity = sum(purchase.mount for purchase in purchases)
    total_amount = sum(purchase.total_price for purchase in purchases)

    response_data = {
        "Mijoz ismi": customer.f_name,
        "Haridlar soni": total_quantity,
        "Umumiy narx": total_amount,
        "1000000 so'mdan yuqorimi": total_amount > 1000000
    }

    return Response(response_data)
