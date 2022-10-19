from rest_framework.test import APITestCase
from . import models


class TestAmenity(APITestCase):
    URL = "/api/v1/rooms/amenities/1/"
    NOTFOUNDURL = "/api/v1/rooms/amenities/2/"
    NAME = "Amen TEST"
    DESC = "Amen DESC"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_get_amenity(self):

        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Status isnt 200")
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get(self.NOTFOUNDURL, {}, True)
        self.assertEqual(response.status_code, 404)

    def test_put_amenity(self):
        baddata = {
            "name": "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss",
            "description": "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss",
        }
        data = {
            "name": "Shower",
            "description": "Showerin",
        }
        response = self.client.put(self.URL, baddata)
        self.assertEqual(response.status_code, 400, "Status code isn't 400 - bad data")
        response = self.client.put(self.URL, data)
        self.assertEqual(response.status_code, 202, "Status code isn't 202")
        self.assertEqual(
            data["name"],
            "Shower",
        )
        self.assertEqual(
            data["description"],
            "Showerin",
        )

    def test_delete_amenity(self):

        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204)


class TestAmenities(APITestCase):

    NAME = "test_name"
    DESC = "test_desc"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status isnt 200")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):

        new_amen_name = "New Amenity"
        new_amen_desc = "New Amen Desc"

        response = self.client.post(
            self.URL,
            data={
                "name": new_amen_name,
                "description": new_amen_desc,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            201,
            "Not 201 CREATED",
        )
        self.assertEqual(
            data["name"],
            new_amen_name,
        )
        self.assertEqual(
            data["description"],
            new_amen_desc,
        )

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            400,
            "No error raised on improper data",
        )
        self.assertIn("name", data)


from users.models import User


class TestRooms(APITestCase):

    URL = "/api/v1/rooms/"

    def setUp(self) -> None:
        bob = User.objects.create(
            username="Bob",
        )
        bob.set_password("123")
        bob.save()
        self.user = bob

    def test_create_room(self):

        res = self.client.post(self.URL)
        self.assertEqual(res.status_code, 403)

        # self.client.login(username="bob", password="123")
        self.client.force_login(user=self.user)
        res = self.client.post(self.URL)
        self.assertEqual(res.status_code, 400)
