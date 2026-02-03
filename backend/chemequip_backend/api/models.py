"""
Models for chemical equipment data visualization app.
"""
from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """
    Model to store uploaded CSV datasets
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='datasets/%Y/%m/%d/')
    
    # Summary statistics stored as JSON
    summary_stats = models.JSONField(default=dict, blank=True)
    
    # Equipment count
    equipment_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Equipment(models.Model):
    """
    Model to store individual equipment records
    """
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Compressor', 'Compressor'),
        ('Heat Exchanger', 'Heat Exchanger'),
        ('Reactor', 'Reactor'),
        ('Separator', 'Separator'),
        ('Column', 'Column'),
        ('Other', 'Other'),
    ]
    
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    flowrate = models.FloatField(null=True, blank=True)  # L/min or similar
    pressure = models.FloatField(null=True, blank=True)  # Bar or similar
    temperature = models.FloatField(null=True, blank=True)  # Celsius
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type})"
