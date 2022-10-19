from functools import partial
from .models import Perk
from .serializers import PerkSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_202_ACCEPTED,
)
from rest_framework.exceptions import NotFound


class Perks(APIView):
    def get(self, req):
        all = Perk.objects.all()
        ser = PerkSerializer(
            all,
            many=True,
        )
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def post(self, req):
        ser = PerkSerializer(
            data=req.data,
        )
        if ser.is_valid():
            new_perk = ser.save()
            return Response(
                PerkSerializer(new_perk).data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class PerkDetail(APIView):
    def go(self, pk):
        try:
            record = Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound
        return record

    def get(self, req, pk):
        perk = self.go(pk)
        ser = PerkSerializer(perk)
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def delete(self, req, pk):
        perk = self.go(pk)
        perk.delete()
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def put(self, req, pk):
        perk = self.go(pk)
        ser = PerkSerializer(
            perk,
            data=req.data,
            partial=True,
        )
        if ser.is_valid():
            updated = ser.save()
            return Response(
                PerkSerializer(updated).data,
                status=HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )
