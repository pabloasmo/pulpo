from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django_auth_ldap.backend import LDAPBackend
from django.core.mail import send_mail

import os
from dotenv import load_dotenv
load_dotenv()

@receiver(user_logged_in)
def user_add_to_bloggers(sender, request, user, **kwargs):
    ldap_backend = LDAPBackend()
    ldap_user = ldap_backend.populate_user(user.username)

    if ldap_user:
        ldap_groups = ldap_user.ldap_user.group_names
        if "bloggers" in ldap_groups:
            bloggers_group, created = Group.objects.get_or_create(name="Bloggers")
            user.groups.add(bloggers_group)
            user.save()
            send_mail(
                subject="Has sido registrado en el grupo bloggers",
                message="Se ha agregado tu usuario al grupo Bloggers en el CMS de la página. Felicidades.",
                from_email=os.getenv("EMAIL_HOST_USER"),
                recipient_list=[user.email],
                fail_silently=False
            )