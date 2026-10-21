from django import forms

from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "preview",
            "is_published",
        ]
        labels = {
            "title": "Заголовок",
            "content": "Содержимое",
            "preview": "Изображение для превью",
            "is_published": "Опубликовано",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
            }),
        }

