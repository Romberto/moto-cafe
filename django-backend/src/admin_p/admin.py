from django.contrib import admin

from admin_p.models import TableModel


@admin.register(TableModel)
class AdminTable(admin.ModelAdmin):
    pass
