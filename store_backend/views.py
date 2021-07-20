# from django.shortcuts import render
from .models import User
from django.views.generic import View
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def sample(request):
    return JsonResponse({1: 'hi'})


class LogInPageView(View):
    def get(self, request):
        return JsonResponse({1: 'hi'})

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
