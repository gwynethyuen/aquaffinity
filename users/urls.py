# users/urls.py
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from users import views as user_views
from django.urls import path

urlpatterns = [
    # default accounts path, login, and logout
    path("accounts/", include("django.contrib.auth.urls")),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/homepage.html'), name='logout'),

    # original path is dashboard homepage
    path("", user_views.dashboard, name="dashboard"),

    # path for registering a user
    path("register/", user_views.register, name="register"),

    # these paths require staff account to view requests and user info
    path("see_request/", user_views.see_request),
    path("user_info/", user_views.user_info),

    # these paths are used to view the different navigation tabs
    path("team/", user_views.team_index, name="team_index"),
    path("swimmer/<int:pk>/", user_views.swimmer_detail, name="swimmer_detail"),
    path("discussion/", user_views.discussion_index, name="discussion_index"),
    path("discussion/<int:pk>/", user_views.discussion_detail, name="discussion_detail"),
    path("discussion/category/<category>/", user_views.discussion_category, name="discussion_category"),
]