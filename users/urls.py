# users/urls.py

from django.conf.urls import include, url
# from users.views import dashboard, register
from users import views as user_views
from django.urls import path
from django.contrib.auth import views as auth_views
# from discussion import views as disc_views
# from swimmers import views as swim_views
# from users.views import homepage
# from django.conf.urls import include, url
# from users.views import dashboard, register

urlpatterns = [
    # path(r"^accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/homepage.html'), name='logout'),
    path("", user_views.dashboard, name="dashboard"),
    path("register/", user_views.register, name="register"),
    path("see_request/", user_views.see_request),
    path("user_info/", user_views.user_info),
    path("add_messages/", user_views.add_messages),
    # path('homepage/', user_views.homepage, name="homepage"),
    path("team/", user_views.team_index, name="team_index"),
    path("swimmer/<int:pk>/", user_views.swimmer_detail, name="swimmer_detail"),
    path("discussion/", user_views.discussion_index, name="discussion_index"),
    path("discussion/<int:pk>/", user_views.discussion_detail, name="discussion_detail"),
    path("discussion/category/<category>/", user_views.discussion_category, name="discussion_category"),
    path("discussion/create/", user_views.discussion_create, name="discussion_create"),
]