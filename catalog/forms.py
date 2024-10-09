from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control "


class ProductForm(StyleFormMixin, forms.ModelForm):
    FORBIDDEN_WORDS = {'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'}

    class Meta:
        model = Product
        fields = ('name', 'description', 'preview', 'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')

        if cleaned_data is None:
            return None

        if any(word in cleaned_data.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError(
                f"В описании не могут быть слова: {', '.join(self.FORBIDDEN_WORDS)}.")
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')

        if cleaned_data is None:
            return None

        if any(word in cleaned_data.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError(
                f"В описании не могут быть слова: {', '.join(self.FORBIDDEN_WORDS)}.")
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
    #
    # def clean_count(self):
    #     cleaned_data = super().clean()
    #     is_active = self.cleaned_data.get('is_active')
    #     product = self.cleaned_data.get('product')
    #
    #     if product:
    #         active_versions_count = Version.objects.filter(product=product, is_active=True).count()
    #
    #         if is_active in active_versions_count >= 1:
    #             raise forms.ValidationError("Только одна версия может быть активной. Пожалуйста, выберите только одну активную версию.")
    #
    #     return cleaned_data
