from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user__username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse_lazy('home')


class RoleRequiredMixin(AccessMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.required_role or request.user.profile.role != self.required_role:
            return redirect('accounts:permission_denied')
        return super().dispatch(request, *args, **kwargs)


def permission_denied(request):
    return render(request, 'accounts/permission_denied.html')
