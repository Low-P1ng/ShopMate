from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    query = request.GET.get('item_name', '').strip()
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products, 'search_query': query})

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'myapp/detail.html', {'product': product})