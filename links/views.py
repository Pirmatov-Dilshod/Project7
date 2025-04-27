import random, string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Link
from .forms import LinkForm
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            
            # Проверяем, существует ли уже ссылка
            existing_link = Link.objects.filter(original_url=original_url).first()
            if existing_link:
                messages.info(request, f'Эта ссылка уже есть! Короткая ссылка: {existing_link.short_code}')
                return redirect('link_list')
            
            # Иначе создаём новую ссылку
            link = form.save(commit=False)
            link.short_code = generate_short_code()
            
            # Защита от совпадений коротких кодов
            while Link.objects.filter(short_code=link.short_code).exists():
                link.short_code = generate_short_code()
            
            link.save()
            messages.success(request, 'Ссылка успешно создана!')
            return redirect('link_list')
    else:
        form = LinkForm()
    return render(request, 'links/create_link.html', {'form': form})

def redirect_link(request, code):
    link = get_object_or_404(Link, short_code=code)
    link.click_count += 1
    link.save()
    return redirect(link.original_url)

def link_list(request):
    links = Link.objects.order_by('-created_at')
    return render(request, 'links/link_list.html', {'links': links})

def delete_old_links(request):
    days = 30  # Удалить старше 30 дней
    cutoff_date = timezone.now() - timedelta(days=days)
    old_links = Link.objects.filter(created_at__lt=cutoff_date)
    count = old_links.count()
    old_links.delete()
    messages.success(request, f"Удалено {count} ссылок старше {days} дней.")
    return redirect('link_list')

@require_POST
def delete_selected_links(request):
    selected_ids = request.POST.getlist('selected_links')
    if selected_ids:
        links_to_delete = Link.objects.filter(id__in=selected_ids)
        count = links_to_delete.count()
        links_to_delete.delete()
        messages.success(request, f"Удалено {count} выбранных ссылок.")
    else:
        messages.warning(request, "Вы не выбрали ни одной ссылки.")
    return redirect('link_list')