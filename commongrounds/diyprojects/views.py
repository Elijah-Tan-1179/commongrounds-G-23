from .models import ProjectCategory, Project
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class ProjectListView(ListView):
    model = ProjectCategory
    template_name = 'diyprojects/project_list.html'

    def get_queryset(self):
        return ProjectCategory.objects.prefetch_related('project_set').all()


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'
