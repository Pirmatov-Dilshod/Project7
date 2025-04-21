import random, string
from django.shortcuts import render, redirect, get_object_or_404
from .models import Link
from .forms import LinkForm

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.short_code = generate_short_code()
            link.save()
            return render(request, 'links/success.html', {'short_code': link.short_code})
    else:
        form = LinkForm()
    return render(request, 'links/create_link.html', {'form': form})

def redirect_link(request, code):
    link = get_object_or_404(Link, short_code=code)
    return redirect(link.original_url)
