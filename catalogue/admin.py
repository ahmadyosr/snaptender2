from django.contrib import admin
from catalogue.models import Snippet, Category, Publisher, Newspaper

# Register your models here.
admin.site.register(Newspaper)
admin.site.register(Snippet)
admin.site.register(Category)
admin.site.register(Publisher)