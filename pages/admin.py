from django.contrib import admin
from pages.models import Page, Category, Comment


class AdminPage(admin.ModelAdmin):
    list_display = ["book_name","user_name"]


admin.site.register(Page,AdminPage)


admin.site.register(Category)
admin.site.register(Comment)


