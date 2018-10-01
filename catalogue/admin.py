from django.contrib import admin
from catalogue.models import TenderSnippet, Category, Publisher

# Register your models here.
admin.site.register(TenderSnippet)
admin.site.register(Category)
admin.site.register(Publisher)