from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import transaction




class Admin(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='admin', verbose_name='Status')

    def __str__(self) -> str:
        return self.name
    
class Customer(models.Model):
    f_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Ism')
    l_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Familiya')
    age = models.PositiveIntegerField(null=True, blank=True,verbose_name='Yoshi')

    def __str__(self) -> str:
        return f"{self.f_name} {self.l_name}"

class Category(models.Model):
    category_name = models.CharField(max_length=100,verbose_name='Maxsulot kategoriyasi')
    
    def __str__(self) -> str:
        return self.category_name
    
class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    name = models.TextField(max_length=100,null=False, blank=False,verbose_name='Maxsulot nomi')
    create_time = models.DateTimeField(verbose_name='Ishlab chiqarilgan vaqti')
    expiry_date = models.DateTimeField(verbose_name='Yaroqlilik muddati')
    quantity = models.PositiveIntegerField()
    price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if Product.objects.exclude(id=self.id).filter(name=self.name).exists():
            raise ValidationError("Bu nom bilan maxsulot allaqachon mavjud.")
    
class ShopCart(models.Model):
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_money = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.customer_name}ning kartasida {self.total_money} puli bor."
    
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.customer} --> {str(self.date)}dagi oderi"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mount = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    card_id = models.ForeignKey(ShopCart,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product} {self.mount} miqdorda {self.order}"
    
    #tanlangan maxsulotni narxini olib keladi agar maxsulot narxi kiritilmasa o'zi defaultda yozad va producdan olingan maxsulotni quantitydan ayiradi
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.product.price * self.mount

        product_price = self.product.price * self.mount
        if self.total_price != product_price:
            raise ValidationError("Maxsulot narxi noto'g'ri")

        if self.mount > self.product.quantity:
            raise ValidationError("Maxsulotlar miqdori yetarli emas")

        self.product.quantity -= self.mount
        self.product.save()

        super().save(*args, **kwargs)

    

    #tanlangan maxsulotni narxini tekshirib shopcarddan pul yechiladi
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.product.price * self.mount

        product_price = self.product.price * self.mount
        if self.total_price != product_price:
            raise ValidationError("Maxsulot narxi noto'g'ri")

        if self.mount > self.product.quantity:
            raise ValidationError("Maxsulotlar miqdori yetarli emas")

        with transaction.atomic():
            self.card_id.total_money -= self.total_price
            self.card_id.save()

            self.product.quantity -= self.mount 
            self.product.save()

            super().save(*args, **kwargs)
