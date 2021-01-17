from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class Customer(models.Model):
    user            = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    dateCreated     = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user.first_name)


class Category(models.Model):
    category = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.category



class Product(models.Model):
    recommend   = models.BooleanField(blank=True, null=True)
    title       = models.CharField(max_length=70, null=True, blank=True)
    condition   = models.CharField(max_length=15, null=True, blank=True )
    producent   = models.CharField(max_length=40, null=True, blank=True)
    stock       = models.PositiveIntegerField(null=True, blank=True)
    priceNormal = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    pricePromo  = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    description = RichTextField()
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags        = TaggableManager()
    pic1        = models.ImageField(null=True, blank=True)
    pic2        = models.ImageField(null=True, blank=True)
    pic3        = models.ImageField(null=True, blank=True, default='logo2.png')
    pic4        = models.ImageField(null=True, blank=True, default='logo2.png')

    def __str__(self):
        return str(self.title )+ " " + str(self.condition) 















class Order(models.Model):
    customer        = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_oredred    = models.DateField(auto_now_add=True)
    complete        = models.BooleanField(default=False, null=True, blank=True)
    transaction_id  = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer.user.first_name)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([x.get_total for x in items])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total




class OrderItem(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order       = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity    = models.IntegerField(default=0, null=True, blank=True)
    date_added  = models.DateTimeField(auto_now_add=True)
    transaction_id  = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        if self.product.pricePromo is None:
            total = self.product.priceNormal * self.quantity
        else:
            total = self.product.pricePromo * self.quantity
        
        return total




class ShipmentMethod(models.Model):
    contractor   = models.CharField(max_length=15, null=True, blank=True )
    price        = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return str(self.contractor)


class ShippingAddress(models.Model):
    customer      = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order         = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    recipient     = models.TextField(max_length=50, null=True)
    city          = models.TextField(max_length=50, null=True)
    country       = models.TextField(max_length=50, null=True)
    zip_code      = models.TextField(max_length=15, null=True)
    phone         = models.TextField(max_length=10, null=True)
    email         = models.EmailField(max_length=30, null=True)
    adress        = models.TextField(max_length=100, null=True)
    date_added    = models.TextField(max_length=100,null=True)
    invoice       = models.BooleanField(default=False, blank=True, null=True)
    invoiceRecipient   = models.TextField(max_length=50, null=True, blank=True)
    invoiceAdress = models.TextField(max_length=50, null=True, blank=True)
    invoiceZip    = models.TextField(max_length=15, null=True, blank=True)
    invoiceCity   = models.TextField(max_length=50, null=True, blank=True)
    invoiceNip    = models.TextField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return str(self.adress)







class HelpCategory(models.Model):
    category  = models.CharField(max_length=20,unique=True)
    categoryIcon    = models.TextField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.category
    
class HelpCategoryContent(models.Model):
    category        = models.ForeignKey(HelpCategory, on_delete=models.SET_NULL, blank=True, null=True)
    helpTitle       = models.TextField(max_length=55, null=True, blank=True)
    
    description = RichTextField()

    def __str__(self):
        return str(self.helpTitle)