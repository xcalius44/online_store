from django.db import models

from shop.models import Product

# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="E-mail")
    address = models.CharField(max_length=250, verbose_name="Адреса")
    postal_code = models.CharField(max_length=7, null=True, blank=True, verbose_name="Індекс")
    city = models.CharField(max_length=50, verbose_name="Місто")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
    
    def __str__(self):
        return f"Замовлення №{self.id}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Замовлення")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.RESTRICT, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    