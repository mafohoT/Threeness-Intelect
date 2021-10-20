from . models import UserProfile
from django.db.models import Q


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return UserProfile.objects.get(pk=user_id)
       except UserProfile.DoesNotExist:
          return None


    def authenticate(self, username, password):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username) | Q(id_number=username)
            )
        except UserProfile.DoesNotExist:
            return None

        return user if user.check_password(password) else None
