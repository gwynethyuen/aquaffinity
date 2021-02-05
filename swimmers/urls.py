from django.urls import path
from . import views

urlpatterns = [
    path("", views.team_index, name="team_index"),
    path("<int:pk>/", views.swimmer_detail, name="swimmer_detail"),
]