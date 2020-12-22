from django.contrib import admin
from .models import Account


@admin.register(Account)
class PositionAdmin(admin.ModelAdmin):
    pass
