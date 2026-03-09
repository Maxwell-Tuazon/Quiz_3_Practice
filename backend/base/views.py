from django.shortcuts import render
from django.http import JsonResponse, Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .products import products as static_products

from .serializers import ProductSerializer
from rest_framework import serializers


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/<id>/',
        '/api/users/login/',
        '/api/users/register/',
    ]
    return JsonResponse(routes, safe=False)


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all().order_by('-createdAt')
    serializer = ProductSerializer(products, many=True)
    db_products = list(serializer.data)

    # Return DB products plus static products together (no deduplication)
    combined = db_products + static_products
    return Response(combined)


@api_view(['GET'])
def getProduct(request, pk):
    # If pk is numeric, try DB first; otherwise treat as static id
    if str(pk).isdigit():
        try:
            product = Product.objects.get(_id=pk)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404
    else:
        # static product id (e.g. 's1')
        for item in static_products:
            if item['_id'] == str(pk):
                return Response(item)
        raise Http404
    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        # include SerializerMethodField names here ('name', '_id', 'isAdmin')
        fields = ['id', 'username', 'email', 'isAdmin', 'name', '_id']
    def get__id(self, obj):
        return obj.id
    def get_isAdmin(self, obj):
        return obj.is_staff
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
