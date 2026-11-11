from PIL import Image, UnidentifiedImageError
from django import forms

from catalog.models import ContactMessage, Product


# Список запрещённых слов
FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_IMAGE_FORMATS = ("JPEG", "PNG")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        labels = {
            "name": "Название продукта",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["name"].widget.attrs["placeholder"] = "Введите название"
        self.fields["description"].widget.attrs["placeholder"] = (
            "Введите описание продукта"
        )
        self.fields["price"].widget.attrs["placeholder"] = "Введите цену"

    def clean_name(self):
        name = self.cleaned_data["name"]
        self._check_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        self._check_forbidden_words(description)
        return description

    @staticmethod
    def _check_forbidden_words(value):
        text = value.casefold()

        for word in FORBIDDEN_WORDS:
            if word.casefold() in text:
                raise forms.ValidationError(
                    f"Текст содержит запрещённое слово: «{word}»."
                )

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. "
                "Укажите нулевую или положительную цену."
            )

        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        if image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )

        try:
            with Image.open(image) as img:
                image_format = img.format
                img.verify()
        except (UnidentifiedImageError, OSError, ValueError):
            raise forms.ValidationError(
                "Загрузите корректное изображение в формате JPEG или PNG."
            )

        if image_format not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError(
                "Разрешены только изображения в формате JPEG или PNG."
            )

        image.seek(0)
        return image


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

        labels = {
            "name": "Ваше имя",
            "email": "Email",
            "message": "Сообщение",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваше имя",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваш email",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваше сообщение",
                    "rows": 5,
                    "required": True,
                }
            ),
        }
