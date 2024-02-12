from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(pre_social_login)
def activate_user_on_social_login(sender, request, sociallogin, **kwargs):
    User = get_user_model()
    user = sociallogin.user
    if not user.is_active:
        user.is_active = True
        user.save()
