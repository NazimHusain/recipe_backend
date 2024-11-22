from django.urls import path
from apps.customuser import views

urlpatterns = [
    path("register/", (views.SignUp.as_view())),
    path("login/", views.UserLogin.as_view()),
    path("logout/", views.UserLogout.as_view())
]