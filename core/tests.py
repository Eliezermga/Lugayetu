from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_preserves_staff_and_superuser_flags_when_saved(self):
        User = get_user_model()
        user = User.objects.create(
            username="staff@example.com",
            email="staff@example.com",
            first_name="Staff",
            last_name="User",
            role="CONTRIBUTOR",
            is_staff=True,
            is_superuser=True,
        )

        user.save()

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
