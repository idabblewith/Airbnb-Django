from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound

from django.contrib.auth import authenticate, login, logout

from .models import User
from . import serializers as user_ser


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        return Response(
            user_ser.PrivateUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    def put(self, req):
        user = req.user
        ser = user_ser.PrivateUserSerializer(
            user,
            data=req.data,
            partial=True,
        )
        if ser.is_valid():
            user = ser.save()
            ser = user_ser.PrivateUserSerializer(user)
            return Response(
                ser.data,
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                ser.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Users(APIView):
    def post(self, req):
        password = req.data.get("password")
        if not password:
            raise ParseError
        ser = user_ser.PrivateUserSerializer(data=req.data)
        if ser.is_valid():
            user = ser.save()
            user.set_password(password)
            user.save()
            ser = user_ser.PrivateUserSerializer(user)
            return Response(
                ser.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PublicUser(APIView):
    def get(self, req, username):
        try:
            user = User.objects.get(username=username)
            ser = user_ser.PrivateUserSerializer(user)
            return Response(
                ser.data,
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            raise NotFound


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user
        old_pass = req.data.get("old_password")
        new_pass = req.data.get("new_password")
        if not old_pass or not new_pass:
            raise ParseError
        if user.check_password(old_pass):
            user.set_password(new_pass)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class Login(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            req,
            username=username,
            password=password,
        )
        if user:
            login(req, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "wrong password"})


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response({"ok": "Bye"})
