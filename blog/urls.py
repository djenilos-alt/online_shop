from django.urls import path

from blog.views import (
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    path("create/", BlogPostCreateView.as_view(), name="post_create"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/update/", BlogPostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="post_delete"),
]
