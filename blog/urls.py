from django.urls import path
from . import views
from django.contrib.auth import views as view


urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("register", views.register, name="register"),
    path("login", view.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout", view.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("profile", views.profile, name="profile")
]