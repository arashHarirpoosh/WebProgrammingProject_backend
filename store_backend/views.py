# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Product, Category
from django.views.generic import View
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout

from store_backend.serializers import ProductSerializer, CategorySerializer
from rest_framework.parsers import JSONParser


# Create your views here.
def sample(request):
    return JsonResponse({1: 'hi'})


@csrf_exempt
def user_logout(request):
    print('logout')
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'logout': True})
    return JsonResponse({'logout': False})


class LogInPageView(View):
    def get(self, request):
        print(request.headers)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return JsonResponse({
                'signIn': True,
                'name': request.user.first_name
            })
        return JsonResponse({
            'signIn': False
        })

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        print(request.headers)
        user_name = body.get('username', False)
        password = body.get('password', False)
        print(user_name, password)
        user = authenticate(request, username=user_name, password=password)
        # user = User.objects.filter(username=user_name).count()
        print(user)
        if user is not None:
            login(request, user)
            print(request.user.is_authenticated)
            user_info = User.objects.get(username=user_name)
            return JsonResponse({'validation': True,
                                 'name': user_info.first_name
                                 })
            # if password == user_info.password:
            #     return JsonResponse({'validation': True,
            #                          'name': user_info.first_name
            #                          })
        return JsonResponse({'validation': False})


class SignUpPageView(View):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        print(body)
        user_existed = User.objects.filter(username=body['email']).count()
        if not user_existed:
            # user = User.objects.create_user(first_name=body['name'], last_name=body['familyName'],
            #                                 username=body['email'], email=body['email'],
            #                                 password=body['password'], address=body['address']
            #                                 )
            # user.password = body['password']
            # user.save()
            user = User.objects.create(first_name=body['name'], last_name=body['familyName'], username=body['email'],
                                       password=body['password'], address=body['address'], email=body['email']
                                       )
            user.set_password(body['password'])
            user.save()

            return JsonResponse({'result': True})

        return JsonResponse({'result': False})


class UserProfile(View):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        if request.user.is_authenticated:
            if body['data'] == 'profile':
                resp = {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    # 'password': request.user.password,
                    'address': request.user.address
                }
                return JsonResponse(resp)

            elif body['data'] == 'receipts':
                return JsonResponse({})
        return JsonResponse({})


class AdminProfile(View):
    def post(self, request):
        # print(request.headers['x-token-access'])

        body = JSONParser().parse(request)
        keys = list(body.keys())
        if 'request' in keys:
            products = Product.objects.all()
            products_serializer = ProductSerializer(products, many=True)
            return JsonResponse(products_serializer.data, safe=False)
        elif 'productName' in keys:
            oldName = body['productName']
            body['productName'] = body['productName2']
            del body['productName2']
            print(body, oldName)
            product = Product.objects.get(productName=oldName)
            product_serializer = ProductSerializer(product, data=body)
            if product_serializer.is_valid():
                product_serializer.save()
                return JsonResponse("Updated Successfully!", safe=False)
            return JsonResponse("Updating Record Failed!", safe=False)


