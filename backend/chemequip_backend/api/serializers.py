"""
Serializers for the API endpoints
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from chemequip_backend.api.models import Dataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model"""
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'created_at']


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Dataset including equipment"""
    equipment = EquipmentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'summary_stats', 'equipment_count', 'equipment', 'user']


class DatasetListSerializer(serializers.ModelSerializer):
    """Serializer for Dataset list view"""
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'equipment_count', 'summary_stats']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    file = serializers.FileField()
    
    def validate_file(self, file):
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        return file


class DataSummarySerializer(serializers.Serializer):
    """Serializer for data summary response"""
    total_equipment = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    equipment_type_distribution = serializers.DictField()
    recent_datasets = DatasetListSerializer(many=True)
