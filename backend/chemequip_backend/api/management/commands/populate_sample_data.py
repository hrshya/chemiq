"""
Django management command to populate sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chemequip_backend.api.models import Dataset, Equipment
from io import StringIO
from chemequip_backend.api.utils import process_csv_file


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'
    
    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='demouser',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('demo123456')
            user.save()
            self.stdout.write(
                self.style.SUCCESS('Created demo user (username: demouser, password: demo123456)')
            )
        else:
            self.stdout.write('Demo user already exists')
        
        # Create sample dataset
        csv_content = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-01,Pump,150.5,10.5,45.2
Pump-02,Pump,200.3,12.0,48.5
Compressor-01,Compressor,300.0,8.5,35.0
Compressor-02,Compressor,275.5,9.2,38.5
Heat Exchanger-01,Heat Exchanger,500.0,6.0,65.5
Heat Exchanger-02,Heat Exchanger,480.5,6.5,68.0
Reactor-01,Reactor,100.0,15.0,80.0
Reactor-02,Reactor,120.5,16.5,85.5
Separator-01,Separator,250.0,7.5,55.0
Separator-02,Separator,280.5,8.0,58.5
Column-01,Column,350.0,5.0,90.0
Column-02,Column,320.5,5.5,92.5
Other-01,Other,150.0,10.0,50.0
Other-02,Other,175.5,11.0,52.5"""
        
        # Create dataset
        dataset, created = Dataset.objects.get_or_create(
            user=user,
            filename='sample_equipment_data.csv',
            defaults={'equipment_count': 0}
        )
        
        if created:
            # Process the CSV content
            from django.core.files.base import ContentFile
            from django.core.files.uploadedfile import InMemoryUploadedFile
            
            # Create an in-memory file
            file_obj = InMemoryUploadedFile(
                StringIO(csv_content),
                field_name='file',
                name='sample_equipment_data.csv',
                content_type='text/csv',
                size=len(csv_content),
                charset='utf-8'
            )
            
            success, message = process_csv_file(file_obj, dataset)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'Created sample dataset with {dataset.equipment_count} equipment items')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Error creating sample dataset: {message}')
                )
        else:
            self.stdout.write('Sample dataset already exists')
        
        self.stdout.write(self.style.SUCCESS('Sample data population complete!'))
