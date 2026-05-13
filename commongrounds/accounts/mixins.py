from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class RoleRequiredMixin(AccessMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.required_role or not request.user.profile.roles.filter(name=self.required_role).exists():
            return redirect('accounts:permission_denied')
        return super().dispatch(request, *args, **kwargs)
    