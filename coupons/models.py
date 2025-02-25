from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код")
    valid_from = models.DateTimeField(verbose_name="Дійсний з")
    valid_to = models.DateTimeField(verbose_name="Дійсний по")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Відсоток знижки (від 0 до 100)',
        verbose_name="Знижка"
    )
    active = models.BooleanField(verbose_name="Активний")

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купони"
    
    def __str__(self):
        return self.code
    