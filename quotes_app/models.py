from django.db import models
from django.core.exceptions import ValidationError


class Source(models.Model):
    SOURCE_TYPES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    type = models.CharField(max_length=10, choices=SOURCE_TYPES, verbose_name="Тип")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"


class Quote(models.Model):
    text = models.TextField(verbose_name="Текст цитаты")
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name="Источник")
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text

    def clean(self):
        # Проверка на дубликаты
        if Quote.objects.filter(text__iexact=self.text).exclude(pk=self.pk).exists():
            raise ValidationError("Такая цитата уже существует")

        # Проверка лимита в 3 цитаты на источник
        if self.pk is None and Quote.objects.filter(source=self.source).count() >= 3:
            raise ValidationError("У источника уже максимальное количество цитат (3)")


class Vote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    is_like = models.BooleanField(verbose_name="Лайк")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"
        unique_together = ['quote', 'ip_address']

    def __str__(self):
        return f"{'👍' if self.is_like else '👎'} для #{self.quote_id}"