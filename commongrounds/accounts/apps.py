from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .models import Role

        def prepopulate_roles(sender, **kwargs):
            for role in Role.roles:
                Role.objects.get_or_create(name=role)

        from django.db.models.signals import post_migrate
        post_migrate.connect(prepopulate_roles, sender=self)