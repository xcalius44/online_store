from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.

def product_list(request: HttpRequest, category_slug: str=None) -> HttpResponse:
    """View для списку товарів"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request, 
        'shop/product/list.html',
        {'category': category,
         'categories': categories,
         'products': products}
    )

def product_detail(request: HttpRequest, id: int, slug: str) -> HttpResponse:
    """View для одного товару"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})