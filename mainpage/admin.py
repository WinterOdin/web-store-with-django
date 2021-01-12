from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
# Register your models here.
from .models import *

class CategoryAdmin(TranslationAdmin):
    pass
class ProductAdmin(TranslationAdmin):
    pass
class HelpCategoryAdmin(TranslationAdmin):
    pass
class HelpCategoryContentAdmin(TranslationAdmin):
    pass

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ShipmentMethod)
admin.site.register(HelpCategory, HelpCategoryAdmin)
admin.site.register(HelpCategoryContent, HelpCategoryContentAdmin)