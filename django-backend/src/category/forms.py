from django import forms

from category.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "название категории"
        self.fields['title'].widget.attrs['class'] = 'form-control mb-2 w-75'
