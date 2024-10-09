from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
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
