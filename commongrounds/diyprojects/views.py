import datetime
from .models import Project
from .forms import ProjectForm, ProjectReviewForm, ProjectRatingForm, FavoriteForm
from .repositories import ProjectRepository
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'
    context_object_name = 'projects'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.repo = ProjectRepository()

    def get_queryset(self):
        return self.repo.get_all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            profile = user.profile

            created = self.repo.get_all().filter(creator=profile)
            favorited = self.repo.get_all().filter(favorite__profile=profile)
            reviewed = self.repo.get_all().filter(projectreview__reviewer=profile)

            user_projects = (created | favorited | reviewed).distinct()

            context['created_projects'] = created
            context['favorited_projects'] = favorited
            context['reviewed_projects'] = reviewed
            context['all_projects'] = self.repo.get_all().exclude(pk__in=user_projects.values('pk'))
        else:
            context['all_projects'] = self.repo.get_all()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.repo = ProjectRepository()

    def get_object(self):
        return self.repo.get_by_id(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        user = self.request.user

        ratings = self.repo.get_ratings(project)
        avg_rating = sum(r.score for r in ratings) / ratings.count() if ratings.exists() else None
        context['avg_rating'] = avg_rating
        context['favorite_count'] = self.repo.get_favorite_count(project)
        context['is_creator'] = user.is_authenticated and project.creator == user.profile
        context['reviews'] = self.repo.get_reviews(project)

        # Pass fresh forms (or re-used invalid ones set by post())
        context.setdefault('rating_form', ProjectRatingForm())
        context.setdefault('review_form', ProjectReviewForm())
        context.setdefault('favorite_form', FavoriteForm())

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        form_type = request.POST.get('form_type')
        profile = request.user.profile

        if form_type == 'rating':
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.profile = profile
                rating.project = self.object
                rating.save()
                return redirect('diyprojects:project_detail', pk=self.object.pk)
            # Re-render with errors
            self.extra_context = {'rating_form': form}

        elif form_type == 'review':
            form = ProjectReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.reviewer = profile
                review.project = self.object
                review.save()
                return redirect('diyprojects:project_detail', pk=self.object.pk)
            self.extra_context = {'review_form': form}

        elif form_type == 'favorite':
            form = FavoriteForm(request.POST)
            if form.is_valid():
                favorite = form.save(commit=False)
                favorite.profile = profile
                favorite.project = self.object
                favorite.date_favorited = datetime.date.today()
                favorite.save()
                return redirect('diyprojects:project_detail', pk=self.object.pk)
            self.extra_context = {'favorite_form': form}

        return self.get(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'diyprojects/project_create.html'
    required_role = 'Project Creator'

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('diyprojects:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Project
    template_name = 'diyprojects/project_update.html'
    required_role = 'Project Creator'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.repo = ProjectRepository()

    def get_object(self):
        return self.repo.get_by_id(self.kwargs['pk'])

    def get_form_class(self):
        return ProjectForm

    def get_success_url(self):
        return reverse_lazy('diyprojects:project_detail', kwargs={'pk': self.object.pk})
