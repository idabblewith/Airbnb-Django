from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth import authenticate, login, logout

from .models import User
from . import serializers as user_ser
import jwt
from django.conf import settings
import requests


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
            return Response(
                {"ok": "welcome"},
                status=HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "wrong password"},
                status=HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response({"ok": "Bye"})


class JWTLogin(APIView):
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
            # Sign token (NO CONFIDENTIAL INFO)
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "Wrong pass"})


class GithubLogin(APIView):
    def post(self, req):
        try:
            code = req.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=b99860fd6028f1114333&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(req, user)
                return Response(status=HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("login"),
                    profile_photo=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                # .has_usable_password() if not social login
                user.save()
                login(req, user)
                return Response(status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                status=HTTP_400_BAD_REQUEST,
            )


# class LineLogin(APIView):
#     def post(self, req):
#         pass
#         # try:
#         #     code = req.data.get("code")
#         #     access_token = requests.post(
#         #         f"https://github.com/login/oauth/access_token?code={code}&client_id=b99860fd6028f1114333&client_secret={settings.GH_SECRET}",
#         #         headers={"Accept": "application/json"},
#         #     )
#         #     access_token = access_token.json().get("access_token")
#         #     user_data = requests.get(
#         #         "https://api.github.com/user",
#         #         headers={
#         #             "Authorization": f"Bearer {access_token}",
#         #             "Accept": "application/json",
#         #         },
#         #     )
#         #     user_data = user_data.json()
#         #     user_emails = requests.get(
#         #         "https://api.github.com/user/emails",
#         #         headers={
#         #             "Authorization": f"Bearer {access_token}",
#         #             "Accept": "application/json",
#         #         },
#         #     )
#         #     user_emails = user_emails.json()
#         #     try:
#         #         user = User.objects.get(email=user_emails[0]["email"])
#         #         login(req, user)
#         #         return Response(status=HTTP_200_OK)
#         #     except User.DoesNotExist:
#         #         user = User.objects.create(
#         #             username=user_data.get("login"),
#         #             email=user_emails[0]["email"],
#         #             name=user_data.get("login"),
#         #             profile_photo=user_data.get("avatar_url"),
#         #         )
#         #         user.set_unusable_password()
#         #         # .has_usable_password() if not social login
#         #         user.save()
#         #         login(req, user)
#         #         return Response(status=HTTP_200_OK)
#         # except Exception as e:
#         #     print(e)
#         #     return Response(
#         #         status=HTTP_400_BAD_REQUEST,
#         #     )
