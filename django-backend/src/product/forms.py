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

        self.fields['photo_url'].label = "url фото"
        self.fields['photo_url'].widget.attrs['class'] = 'form-control mb-2'

        self.fields['description'].label = "краткое описание"
        self.fields['description'].widget.attrs['class'] = 'form-control mb-2'

        self.fields['category'].label = "категория продукта"
        self.fields['category'].widget.attrs['class'] = 'form-select mb-2 w-50'
