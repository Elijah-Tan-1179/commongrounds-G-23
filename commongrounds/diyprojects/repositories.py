from .models import Project, Favorite, ProjectReview, ProjectRating


class ProjectRepository:
    def get_all(self):
        return Project.objects.all()
    
    def get_by_category(self, category_name):
        return Project.objects.filter(category__name=category_name)

    def get_recent(self, n):
        return Project.objects.order_by('-created_on')[:n]

    def get_by_id(self, id):
        return Project.objects.get(pk=id)

    def get_favorite_count(self, project):
        return Favorite.objects.filter(project=project).count()

    def get_reviews(self, project):
        return ProjectReview.objects.filter(project=project)

    def get_ratings(self, project):
        return ProjectRating.objects.filter(project=project)
