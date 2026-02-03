"""
Admin configuration for chemical equipment app
"""
from django.contrib import admin
from chemequip_backend.api.models import Dataset, Equipment


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'equipment_count']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['uploaded_at', 'equipment_count', 'summary_stats']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'filename', 'file', 'uploaded_at')
        }),
        ('Statistics', {
            'fields': ('equipment_count', 'summary_stats')
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset__uploaded_at']
    search_fields = ['name', 'dataset__filename']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Equipment Information', {
            'fields': ('dataset', 'name', 'equipment_type')
        }),
        ('Parameters', {
            'fields': ('flowrate', 'pressure', 'temperature')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
