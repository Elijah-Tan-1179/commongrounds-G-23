from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user__username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'username': self.object.user.username})