from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.sample),
    path('login', csrf_exempt(views.LogInPageView.as_view())),
    path('logout', csrf_exempt(views.user_logout)),
    path('signup', csrf_exempt(views.SignUpPageView.as_view())),
]
