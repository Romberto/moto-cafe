from PIL import Image
from django import forms

from product.models import Product


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

    def clean_image_field(self):
        image = self.cleaned_data.get('photo')

        # Проверяем, что изображение существует
        if image:
            # Открываем изображение с помощью библиотеки PIL (Pillow)
            img = Image.open(image)

            # Изменяем размер изображения, сохраняя пропорции
            max_size = (800, 600)  # Замените на желаемые размеры
            img.thumbnail(max_size)

            # Сохраняем измененное изображение
            img.save(image.path)

        return image
