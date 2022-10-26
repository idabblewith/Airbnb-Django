from bookings.models import Booking
from medias.models import Photo
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from django.db import transaction
from reviews.serializers import ReviewSerializer
from django.conf import settings
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from django.utils import timezone

import time


class Amenities(APIView):
    def get(self, req):
        all = Amenity.objects.all()
        ser = AmenitySerializer(all, many=True)
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def post(self, req):
        ser = AmenitySerializer(data=req.data)
        if ser.is_valid():
            a = ser.save()
            return Response(
                AmenitySerializer(a).data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def go(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        a = self.go(pk)
        ser = AmenitySerializer(a)
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def delete(self, req, pk):
        a = self.go(pk)
        a.delete()
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def put(self, req, pk):
        a = self.go(pk)
        ser = AmenitySerializer(
            a,
            data=req.data,
            partial=True,
        )
        if ser.is_valid():
            ua = ser.save()
            return Response(
                AmenitySerializer(ua).data,
                status=HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                status=HTTP_400_BAD_REQUEST,
            )


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req):
        all = Room.objects.all()
        ser = RoomListSerializer(
            all,
            many=True,
            context={"request": req},
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def post(self, req):
        ser = RoomDetailSerializer(
            data=req.data,
        )
        if ser.is_valid():
            category_pk = req.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category kind should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found!")
            try:
                with transaction.atomic():
                    new_room = ser.save(
                        owner=req.user,
                        category=category,
                    )
                    amenities = req.data.get("amenities")
                    for ame_pk in amenities:
                        amenity = Amenity.objects.get(pk=ame_pk)
                        new_room.amenities.add(amenity)
                    ser = RoomDetailSerializer(
                        new_room,
                        context={"request": req},
                    )
                    return Response(
                        ser.data,
                        status=HTTP_201_CREATED,
                    )
            except Exception as e:
                print(e)
                raise ParseError("Amenity not found")

        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):
    # time.sleep(3)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def go(self, pk):
        try:
            obj = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        return obj

    def get(self, req, pk):
        obj = self.go(pk)
        ser = RoomDetailSerializer(
            obj,
            context={"request": req},
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def delete(self, req, pk):
        room = self.go(pk)
        if room.owner != req.user:
            raise PermissionDenied
        room.delete()
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def put(self, req, pk):
        room = self.go(pk)
        if room.owner != req.user:
            raise PermissionDenied
        ser = RoomDetailSerializer(
            room,
            data=req.data,
            partial=True,
        )
        if ser.is_valid():
            upd = ser.save()
            return Response(
                RoomDetailSerializer(upd).data,
                status=HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def go(self, pk):
        try:
            obj = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        return obj

    def get(self, req, pk):
        try:
            page = req.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            # If user sends asdbaishdgba as page
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.go(pk)
        ser = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def post(self, req, pk):
        ser = ReviewSerializer(data=req.data)
        if ser.is_valid():
            review = ser.save(
                user=req.user,
                room=self.go(pk),
            )
            ser = ReviewSerializer(review)
            return Response(
                ser.data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomAmenities(APIView):
    def go(self, pk):
        try:
            obj = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        return obj

    def get(self, req, pk):
        try:
            page = req.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            # If user sends asdbaishdgba as page
            page = 1
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        room = self.go(pk)
        ser = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )


class RoomPhotos(APIView):
    # {"file": "http://localhost:8000/api/v1/rooms/2/photos", "description": "yoo"}

    permission_classes = [IsAuthenticatedOrReadOnly]

    def go(self, pk):
        try:
            room = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        return room

    def post(self, req, pk):
        room = self.go(pk)
        # print(req.user.is_authenticated)
        # print(req.user)
        if req.user != room.owner:
            raise PermissionDenied

        ser = PhotoSerializer(
            data=req.data,
        )
        if ser.is_valid():
            photo = ser.save(room=room)
            ser = PhotoSerializer(photo)
            return Response(
                ser.data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def go(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        room = self.go(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        ser = PublicBookingSerializer(
            bookings,
            many=True,
            context={"request": req},
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def post(self, req, pk):
        room = self.go(pk)
        ser = CreateRoomBookingSerializer(data=req.data)
        if ser.is_valid():
            booking = ser.save(
                room=room,
                user=req.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            ser = PublicBookingSerializer(booking)
            return Response(
                ser.data,
            )
        else:
            return Response(
                ser.errors,
            )
