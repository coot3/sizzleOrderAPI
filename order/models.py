from django.db import models

# Create your models here.
class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Burger', 'Burger'),
        ('Side', 'Side'),
        ('Beverage', 'Beverage'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='products/', height_field=None, width_field=None, max_length=None)
    on_special = models.BooleanField(default=False)
    special_text = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    order_no = models.IntegerField()
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.order_no)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.product} ({self.qty})"



