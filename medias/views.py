from rest_framework.views import APIView
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import requests


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def go(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, req, pk):
        photo = self.go(pk)

        # if (photo.room and photo.room.owner != req.user) or (
        #     photo.experience and photo.experience.host != req.user
        # ):
        #     raise PermissionDenied
        photo.delete()
        return Response(
            status=HTTP_204_NO_CONTENT,
        )


class GetUploadURL(APIView):
    def post(self, req):
        # f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1"

        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_IMAGES_TOKEN}",
                # "Content-Type": "multipart/form-data",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        print(result)
        return Response(
            {
                "uploadURL": result.get("uploadURL"),
            }
        )
