# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Product, Category
from django.views.generic import View
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout

from store_backend.serializers import ProductSerializer, CategorySerializer
from rest_framework.parsers import JSONParser
from django.core import serializers


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
        method = body['method']
        if request.user.is_authenticated:
            if method == 'getProfile':
                resp = {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    # 'email': request.user.email,
                    # 'password': request.user.password,
                    'address': request.user.address,
                    'balance': request.user.balance
                }
                return JsonResponse(resp)

            elif method == 'receipts':
                return JsonResponse({})

            elif method == 'changeBalance':
                user = User.objects.filter(username=request.user.username).get()
                user.balance += 10000
                user.save()
                return JsonResponse({'balance': user.balance})

            elif method == 'edit':
                user = User.objects.filter(username=request.user.username).get()
                edited = False
                if body['name'] is not '':
                    user.first_name = body['name']
                    edited = edited or True

                if body['familyName'] is not '':
                    user.last_name = body['familyName']
                    edited = edited or True

                if body['password'] is not '':
                    user.set_password(body['password'])
                    edited = edited or True

                if body['address'] is not '':
                    user.address = body['address']
                    edited = edited or True
                if edited:
                    user.save()
                print(body)
                resp = {
                    'result': True,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'address': request.user.address,
                }
                return JsonResponse(resp)

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
        elif 'editPro' in keys:
            del body['editPro']
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

        elif 'createPro' in keys:
            del body['createPro']
            body_serializer = ProductSerializer(data=body)
            if body_serializer.is_valid():
                body_serializer.save()
                return JsonResponse("Added Successfully!", safe=False)
            return JsonResponse("Failed to Add!", safe=False)

        elif 'categories' in keys:
            del body['categories']
            categories = Category.objects.all()
            categories_serializer = CategorySerializer(categories, many=True)
            return JsonResponse(categories_serializer.data, safe=False)


class SendProducts(View):
    def get(self, request):
        num_of_products = Product.objects.count()
        return JsonResponse({'numProducts': num_of_products})

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        method = body['method']
        if method == 'pagination':
            print(body)
            page_num = body['pageNumber']
            products = Product.objects.order_by(body['order'])[14 * (page_num - 1):14 * page_num]
            products_array = json.loads(serializers.serialize('json', products))
            resp = []
            for p in products_array:
                resp.append(p['fields'])
            print(resp)
            return JsonResponse({'products': resp})
        elif method == 'search':
            print(body)
            search_res = Product.objects.filter(productName__contains=body['searchParam'])
            products_array = json.loads(serializers.serialize('json', search_res))
            resp = []
            for p in products_array:
                resp.append(p['fields'])
            print(search_res)
            print(resp)
            return JsonResponse({'products': resp})

        return JsonResponse({})
