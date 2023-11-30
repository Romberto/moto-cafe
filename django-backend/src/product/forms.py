from PIL import Image
from django import forms

from product.models import Product
from django.core.exceptions import ValidationError


def photo_valid(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['png', 'jpg', 'jpeg']:
        raise ValidationError("расширение файла может быть 'png', 'jpg', 'jpeg'")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "название продукта"
        self.fields['title'].widget.attrs['class'] = 'form-control mb-2 w-75'

        self.fields['price'].label = "цена"
        self.fields['price'].widget.attrs['class'] = 'form-control mb-2 w-50'

        self.fields['photo'].label = 'загрузите фото 800х600px'
        self.fields['photo'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['photo'].help_text = '800х600px или кратное этим размерам'

        self.fields['description'].label = "краткое описание"
        self.fields['description'].widget.attrs['class'] = 'form-control mb-2'

        self.fields['times'].label = "время приготовления"
        self.fields['times'].widget.attrs['class'] = 'form-control mb-2'

        self.fields['category'].label = "категория продукта"
        self.fields['category'].widget.attrs['class'] = 'form-select mb-2 w-50'

    photo = forms.ImageField(validators=[photo_valid])
