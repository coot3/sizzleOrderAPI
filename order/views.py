from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer


class ProductsAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderAPI(APIView):
    def post(self, request):
        last_order = Order.objects.last()
        if not last_order or last_order.order_no == 99:
            new_order = Order.objects.create(order_no=1)
            new_order.save()
        else:
            new_order = Order.objects.create(order_no=last_order.order_no + 1)
            new_order.save()
        for item in request.data:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(order=new_order, product=product, qty=item['qty'])
        data = {
            'order_no': new_order.order_no
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CurrentOrdersAPI(APIView):
    def get(self, request):
        orders = Order.objects.filter(completed=False)
        serializer = OrderSerializer(instance=orders, many=True)
        for order in serializer.data:
            order_object = Order.objects.get(id=order['id'])
            order_items = order_object.orderitem_set.filter(order=order_object)
            order_item_serializer = OrderItemSerializer(data=order_items, many=True)
            order_item_serializer.is_valid()
            order['order_items'] = order_item_serializer.data
        return Response(serializer.data)

    def post (self, request):
        completed_order = Order.objects.get(id=request.data['id'])
        completed_order.completed = True
        completed_order.save()
        
        orders = Order.objects.filter(completed=False)
        serializer = OrderSerializer(instance=orders, many=True)
        for order in serializer.data:
            order_object = Order.objects.get(id=order['id'])
            order_items = order_object.orderitem_set.filter(order=order_object)
            order_item_serializer = OrderItemSerializer(data=order_items, many=True)
            order_item_serializer.is_valid()
            order['order_items'] = order_item_serializer.data
        return Response(serializer.data)

# Create your views here.

