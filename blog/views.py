from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import BlogPostForm
from blog.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.has_perm("blog.view_blogpost"):
            return BlogPost.objects.all().order_by("-created_at")

        return BlogPost.objects.filter(
            is_published=True
        ).order_by("-created_at")


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.has_perm("blog.view_blogpost"):
            return BlogPost.objects.all()

        return BlogPost.objects.filter(is_published=True)

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        post.views_count += 1
        post.save(update_fields=["views_count"])
        return post


class BlogPostCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:post_list")
    permission_required = "blog.add_blogpost"


class BlogPostUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    permission_required = "blog.change_blogpost"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    permission_required = "blog.delete_blogpost"
