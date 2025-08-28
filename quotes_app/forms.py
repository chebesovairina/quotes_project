from django import forms
from .models import Quote, Source


class QuoteForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'style': 'width: 100%;'}),
        label="Текст цитаты"
    )
    source_type = forms.ChoiceField(
        choices=Source.SOURCE_TYPES,
        label="Тип источника"
    )
    source_name = forms.CharField(
        max_length=200,
        label="Название источника"
    )
    weight = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        label="Вес (1-100)",
        help_text="Чем выше вес, тем чаще показывается цитата"
    )

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')

        if source_name and source_type:
            # Проверяем лимит цитат для существующего источника
            try:
                source = Source.objects.get(name=source_name, type=source_type)
                if Quote.objects.filter(source=source).count() >= 3:
                    raise forms.ValidationError(
                        f"У источника '{source}' уже максимальное количество цитат (3)"
                    )
            except Source.DoesNotExist:
                # Источник не существует - можно создавать
                pass

        # Проверка на дубликаты цитат
        text = cleaned_data.get('text')
        if text and Quote.objects.filter(text__iexact=text).exists():
            raise forms.ValidationError("Такая цитата уже существует")

        return cleaned_data

    def save(self):
        source_name = self.cleaned_data['source_name']
        source_type = self.cleaned_data['source_type']
        text = self.cleaned_data['text']
        weight = self.cleaned_data['weight']

        # Создаем или получаем источник
        source, created = Source.objects.get_or_create(
            name=source_name,
            type=source_type,
            defaults={'name': source_name, 'type': source_type}
        )

        # Создаем цитату
        quote = Quote.objects.create(
            text=text,
            source=source,
            weight=weight
        )

        return quote