from django.urls import path
from . import views

urlpatterns = [
    path(
        "requests",
        views.commission_list,
        name="commission_list",
    ),
    path(
        "request/<int:pk>",
        views.commission_detail,
        name="commission_detail",
    ),
]