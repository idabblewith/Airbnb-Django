from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_202_ACCEPTED,
)
from .models import Wishlist
from rooms.models import Room
from .serializers import WishlistSerializer


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        all_wishlists = Wishlist.objects.filter(user=req.user)
        ser = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": req},
        )
        return Response(ser.data, status=HTTP_200_OK)

    def post(self, req):
        ser = WishlistSerializer(data=req.data)
        if ser.is_valid():
            wl = ser.save(
                user=req.user,
            )
            ser = WishlistSerializer(wl)
            return Response(
                ser.data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def go(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        wl = self.go(pk, req.user)
        print(f"\n\n{wl}\n\n")
        ser = WishlistSerializer(
            wl,
            context={"request": req},
        )
        print(f"\n\n{ser}\n\n")

        print(f"\n\n{req.user}\n\n")
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def delete(self, req, pk):
        wl = self.go(pk, user=req.user)
        wl.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, req, pk):
        wl = self.go(pk=pk, user=req.user)
        ser = WishlistSerializer(
            wl,
            data=req.data,
            partial=True,
        )
        if ser.is_valid():
            wl = ser.save()
            ser = WishlistSerializer(
                wl,
            )
            return Response(
                ser.data,
                status=HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class WishlistToggle(APIView):

    permission_classes = [IsAuthenticated]

    def go(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, req, pk, room_pk):
        list = self.go(pk, req.user)
        room = self.get_room(room_pk)

        if list.rooms.filter(pk=room.pk).exists():
            list.rooms.remove(room)
        else:
            list.rooms.add(room)

        return Response(status=HTTP_202_ACCEPTED)


# {"name":"Vacation in Greece"}
