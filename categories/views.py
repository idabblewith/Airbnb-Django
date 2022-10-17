from .models import Category
from .serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)


class Categories(APIView):
    def get(self, req):
        all_cat = Category.objects.all()
        serializer = CategorySerializer(
            all_cat,
            many=True,
        )
        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )

    def post(self, req):
        serializer = CategorySerializer(data=req.data)
        if serializer.is_valid():
            new_cat = serializer.save()
            return Response(
                CategorySerializer(new_cat).data,
                status=201,
            )
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_obj(self, pk):
        try:
            record = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return record

    def get(self, req, pk):
        ser = CategorySerializer(self.get_obj(pk))
        return Response(
            ser.data,
            status=HTTP_200_OK,
        )

    def delete(self, req, pk):
        cat = self.get_obj(pk)
        cat.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, req, pk):
        ser = CategorySerializer(
            self.get_obj(pk=pk),
            req.data,
            partial=True,
        )
        if ser.is_valid():
            updated = ser.save()
            return Response(
                CategorySerializer(updated).data,
                status=HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                ser.errors,
                status=HTTP_400_BAD_REQUEST,
            )
