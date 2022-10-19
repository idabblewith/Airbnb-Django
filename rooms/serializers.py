from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist

# {
#     "name": "Workin",
#     "country": "Australia",
#     "city": "Perth",
#     "price": 0,
#     "rooms": 2,
#     "toilets": 1,
#     "description": "A Room",
#     "address": "Perth, Australia",
#     "pet_friendly": true,
#     "kind": "private_room",
#       "category": 1,
#       "amenities": [2,]
# }


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name", "description"]


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        ]

    def get_is_owner(self, room):
        req = self.context["request"]
        return room.owner == req.user

    def get_rating(self, room):
        return room.rating()


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    # amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["request"]
        return room.owner == req.user

    def get_is_liked(self, room):
        req = self.context["request"]
        return Wishlist.objects.filter(user=req.user, rooms__id=room.pk).exists()
