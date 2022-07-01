from django.test import TestCase

from tenant.models import Tenant
from user.models import User
from user.serializer import UserSerializer


class UserTest(TestCase):
    def setUp(self):
        tenant = Tenant.objects.create(
            name="element5",
            description="product"
        )

        user = User.objects.create(
            name="vignesh",
            email="vignesh@gmail.com",
            phone_number=9122342342,
            user_role="subscriber"
        )

    def test_create_user(self):
        payload = {
            "name": "arun",
            "email": "arun@gmail.com",
            "phone_number": 9180898879,
            "password": "arun@1234",
            "user_role": "subscriber"
        }

        user = UserSerializer(data=payload)
        user.is_valid(raise_exception=True)
        user.save()

        self.assertEqual(user.data["id"], 2)
        self.assertEqual(user.data["name"], "arun")
        self.assertEqual(user.data["phone_number"], 9180898879)
        self.assertEqual(user.data["email"], "arun@gmail.com")
        self.assertEqual(user.data["user_role"], "subscriber")




