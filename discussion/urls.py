from django.urls import path
from . import views

urlpatterns = [
    path("", views.discussion_index, name="discussion_index"),
    path("<int:pk>/", views.discussion_detail, name="discussion_detail"),
    path("<category>/", views.discussion_category, name="discussion_category"),
]