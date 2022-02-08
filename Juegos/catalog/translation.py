from modeltranslation.translator import translator, TranslationOptions
from .models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


translator.register(Category, CategoryTranslationOptions)
