from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import models
import random
from .models import Quote, Source, Vote
from .forms import QuoteForm


def random_quote(request):
    """Главная страница со случайной цитатой"""
    quotes = Quote.objects.all()

    if quotes.exists():
        # Выбор случайной цитаты с учетом веса
        weights = [quote.weight for quote in quotes]
        random_quote_obj = random.choices(quotes, weights=weights, k=1)[0]

        # Увеличиваем счетчик просмотров
        random_quote_obj.views_count += 1
        random_quote_obj.save()

        # Добавляем счетчики лайков/дизлайков
        random_quote_obj.likes_count = random_quote_obj.votes.filter(is_like=True).count()
        random_quote_obj.dislikes_count = random_quote_obj.votes.filter(is_like=False).count()
    else:
        random_quote_obj = None

    return render(request, 'quotes_app/random_quote.html', {
        'quote': random_quote_obj
    })


def add_quote(request):
    """Страница добавления новой цитаты"""
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Цитата успешно добавлена!')
                return redirect('random_quote')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {str(e)}')
    else:
        form = QuoteForm()

    return render(request, 'quotes_app/add_quote.html', {'form': form})


def popular_quotes(request):
    """Страница с популярными цитатами"""
    # Берем 10 самых популярных по лайкам
    popular = Quote.objects.annotate(
        likes_count=models.Count('votes', filter=models.Q(votes__is_like=True)),
        dislikes_count=models.Count('votes', filter=models.Q(votes__is_like=False))
    ).order_by('-likes_count')[:10]

    return render(request, 'quotes_app/popular_quotes.html', {
        'quotes': popular
    })


@require_POST
def vote(request, quote_id, vote_type):
    """Обработка лайков/дизлайков"""
    quote = get_object_or_404(Quote, id=quote_id)
    ip_address = get_client_ip(request)

    # Проверяем, не голосовал ли уже этот IP
    existing_vote = Vote.objects.filter(quote=quote, ip_address=ip_address).first()

    if existing_vote:
        # Если уже голосовал, обновляем голос
        existing_vote.is_like = (vote_type == 'like')
        existing_vote.save()
    else:
        # Создаем новый голос
        Vote.objects.create(
            quote=quote,
            is_like=(vote_type == 'like'),
            ip_address=ip_address
        )

    # Получаем актуальные счетчики
    likes_count = quote.votes.filter(is_like=True).count()
    dislikes_count = quote.votes.filter(is_like=False).count()

    return JsonResponse({
        'success': True,
        'likes': likes_count,
        'dislikes': dislikes_count
    })


def get_client_ip(request):
    """Получение IP адреса пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def search_quotes(request):
    """Поиск цитат по источнику"""
    sources = Source.objects.all()
    quotes = None
    selected_source = None

    if request.method == 'GET' and 'source_id' in request.GET:
        source_id = request.GET.get('source_id')
        if source_id:
            selected_source = get_object_or_404(Source, id=source_id)
            quotes = Quote.objects.filter(source=selected_source).annotate(
                likes_count=models.Count('votes', filter=models.Q(votes__is_like=True)),
                dislikes_count=models.Count('votes', filter=models.Q(votes__is_like=False))
            ).order_by('-created_at')

    return render(request, 'quotes_app/search_quotes.html', {
        'sources': sources,
        'quotes': quotes,
        'selected_source': selected_source
    })