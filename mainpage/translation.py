from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product,HelpCategory,HelpCategoryContent

class CategoryTranslationOptions(TranslationOptions):
    fields = ('category',)

class ProductTranslationOptions(TranslationOptions):
    fields = ('title','condition','description')

class HelpCategoryTranslationOptions(TranslationOptions):
    fields = ('category',)

class HelpCategoryContentTranslationOptions(TranslationOptions):
    fields = ('helpTitle','description')

translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(HelpCategory, HelpCategoryTranslationOptions)
translator.register(HelpCategoryContent, HelpCategoryContentTranslationOptions)