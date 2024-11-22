from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotAcceptable
from django.db import DatabaseError
from apps.customuser import models as UserModels
from rest_framework.authtoken.models import Token
from apps.helpers import models as coreModels
from django.contrib.auth import login, logout
from apps.customuser import serializers 


class SignUp(APIView):
    """Api for Register User."""

    permission_classes = ()
    authentication_classes = ()

    def post(self: "SignUp", request: Request, *args: any, **kwargs: any) -> Response:
        data = request.data
        try:
            if data.get("email"):
                user = UserModels.User.objects.create_user(
                    username=data.get("email"),
                    email=data.get("email"),
                    password=data.get("password")) 
                
            token, _ = Token.objects.get_or_create(user=user)
            if data.get("first_name"):
                user.first_name = data.get("first_name")
            if data.get("last_name"):
                user.last_name = data.get("last_name")

            if data.get("role"):
                role_slug = data.get("role")
                user.role = coreModels.DropdownValues.objects.get(slug=role_slug)
                
            if data.get("profilePic"):
                user.profilePic = coreModels.FileUpload.objects.get(id=data.get("profilePic"))
            user.save()

            return Response({"key": token.key}, 201)
        except DatabaseError:
            raise NotAcceptable("Username already exists")
        except Exception as e:
            print(str(e))
            raise NotAcceptable("User could not be created, check the data")
        

class UserLogin(APIView):
    """Api for Login User.
    username(str) - username of user
    password(str) - password of user
    """

    permission_classes = []

    def post(self: "UserLogin", request: Request, version: str) -> Response:
        data = request.data
        try:
            data["username"]
        except Exception:
            try:
                data["username"] = data["email"]
            except Exception:
                return Response(
                    {
                        "response": "User created but cannot login, please try login manually."
                    },
                    400,
                )
        data["password"] = data.get("password")
        serialized = serializers.UserLoginSerializer(data=data)
        if serialized.is_valid():
            user = serialized.user
            login(request, user)
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            data, success_code = {
                "key": token.key,
                "role": user.role.slug if user.role.slug else None,
                }, 200
            return Response(data, success_code)
        return Response(serialized.errors)
    
class UserLogout(APIView):
    """APi for logout"""

    def post(self: "UserLogout", request: Request, version: str) -> Response:
        request.auth.delete()
        logout(request)
        data = {"response": "Log out Successfully"}
        return Response(data=data, status=200)
    





