from django.contrib import admin

from tables.models import TableModel


@admin.register(TableModel)
class AdminTable(admin.ModelAdmin):
    pass
