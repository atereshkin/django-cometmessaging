from django.contrib import admin

from .models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    pass

admin.site.register(ToDo, ToDoAdmin)
