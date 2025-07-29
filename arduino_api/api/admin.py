from django.contrib import admin
from .models import LightEvent, LightStatus

@admin.register(LightEvent)
class LightEventAdmin(admin.ModelAdmin):
    list_display = ['stato', 'timestamp']
    list_filter = ['stato', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

@admin.register(LightStatus)
class LightStatusAdmin(admin.ModelAdmin):
    list_display = ['is_on', 'ultimo_cambio', 'soglia']