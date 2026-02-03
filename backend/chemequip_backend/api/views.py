"""
API Views for chemical equipment data visualization
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from django.contrib.auth.models import User
from chemequip_backend.api.models import Dataset, Equipment
from chemequip_backend.api.serializers import (
    DatasetDetailSerializer, DatasetListSerializer, 
    CSVUploadSerializer, DataSummarySerializer, EquipmentSerializer, UserSerializer
)
from chemequip_backend.api.utils import process_csv_file, get_user_summary, calculate_summary_stats
from chemequip_backend.api.pdf_utils import generate_pdf_report
import os


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User registration and management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            email=email or '',
            password=password
        )
        
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Login user and get token
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(username=username).first()
        
        if not user or not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Dataset management and CSV upload
    """
    serializer_class = DatasetDetailSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """
        Return datasets for the current user
        """
        return Dataset.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views
        """
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetDetailSerializer
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        """
        Handle CSV file upload
        """
        serializer = CSVUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = serializer.validated_data['file']
        
        # Create Dataset instance
        dataset = Dataset.objects.create(
            user=request.user,
            filename=file_obj.name,
            file=file_obj
        )
        
        # Process CSV
        success, message = process_csv_file(file_obj, dataset)
        
        if not success:
            dataset.delete()
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Keep only last 5 datasets
        all_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if all_datasets.count() > 5:
            old_datasets = all_datasets[5:]
            for old_dataset in old_datasets:
                if old_dataset.file:
                    old_dataset.file.delete()
                old_dataset.delete()
        
        return Response(
            {
                'message': message,
                'dataset': DatasetDetailSerializer(dataset).data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """
        Get all equipment for a specific dataset
        """
        try:
            dataset = Dataset.objects.get(id=pk, user=request.user)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        equipment = Equipment.objects.filter(dataset=dataset)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        Get summary statistics for a specific dataset
        """
        try:
            dataset = Dataset.objects.get(id=pk, user=request.user)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

        stats = calculate_summary_stats(dataset)

        # Adapt keys to the desktop client expectations
        summary_payload = {
            'count': stats.get('total_equipment', 0),
            'averages': {
                'flowrate': stats.get('avg_flowrate'),
                'pressure': stats.get('avg_pressure'),
                'temperature': stats.get('avg_temperature'),
            },
            'type_distribution': stats.get('equipment_type_distribution', {}),
        }

        return Response(summary_payload)
    
    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        """
        Generate and download PDF report for a dataset
        """
        buffer, message = generate_pdf_report(pk, request.user)
        
        if buffer is None:
            return Response(
                {'error': message},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get dataset for filename
        dataset = Dataset.objects.get(id=pk, user=request.user)
        filename = f"Report_{dataset.filename.replace('.csv', '')}.pdf"
        
        response = FileResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class SummaryViewSet(viewsets.ViewSet):
    """
    ViewSet for data summary and analytics
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary statistics for all user's data
        """
        summary = get_user_summary(request.user)
        
        # Serialize datasets
        from chemequip_backend.api.serializers import DatasetListSerializer
        summary['recent_datasets'] = DatasetListSerializer(
            summary['recent_datasets'],
            many=True
        ).data
        
        return Response(summary)


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Equipment (read-only)
    """
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return equipment for datasets of the current user
        """
        return Equipment.objects.filter(dataset__user=self.request.user)
