from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # очистка кошика
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['first_name'] = request.user.first_name
            initial['last_name'] = request.user.last_name
            initial['email'] = request.user.email
        form = OrderCreateForm(initial=initial)
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})