# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User
from django.views.generic import View
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout


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
