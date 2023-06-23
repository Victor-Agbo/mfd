from django.contrib import admin
from django.contrib.admin.models import LogEntry
from . import models

# Register your models here.


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action_time")


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.User)
