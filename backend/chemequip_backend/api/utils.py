"""
Utility functions for CSV processing and analytics
"""
import pandas as pd
import io
from django.core.files.base import ContentFile
from chemequip_backend.api.models import Equipment, Dataset
from collections import defaultdict, Counter


def process_csv_file(file_obj, dataset_instance):
    """
    Process uploaded CSV file and create Equipment records
    
    Expected CSV columns:
    - Equipment Name
    - Type
    - Flowrate
    - Pressure
    - Temperature
    """
    try:
        # Reset file pointer to the beginning
        file_obj.seek(0)
        # Read CSV file
        file_content = file_obj.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(file_content))
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_columns):
            return False, f"CSV must contain columns: {', '.join(required_columns)}"
        
        # Clear existing equipment for this dataset
        Equipment.objects.filter(dataset=dataset_instance).delete()
        
        # Create Equipment records
        for index, row in df.iterrows():
            try:
                equipment = Equipment.objects.create(
                    dataset=dataset_instance,
                    name=str(row['Equipment Name']).strip(),
                    equipment_type=str(row['Type']).strip(),
                    flowrate=float(row['Flowrate']) if pd.notna(row['Flowrate']) else None,
                    pressure=float(row['Pressure']) if pd.notna(row['Pressure']) else None,
                    temperature=float(row['Temperature']) if pd.notna(row['Temperature']) else None,
                )
            except Exception as e:
                return False, f"Error processing row {index + 1}: {str(e)}"
        
        # Calculate and store summary statistics
        stats = calculate_summary_stats(dataset_instance)
        dataset_instance.summary_stats = stats
        dataset_instance.equipment_count = Equipment.objects.filter(dataset=dataset_instance).count()
        dataset_instance.save()
        
        return True, "CSV processed successfully"
    
    except Exception as e:
        return False, f"Error processing CSV: {str(e)}"


def calculate_summary_stats(dataset_instance):
    """
    Calculate summary statistics for a dataset
    """
    equipment_list = Equipment.objects.filter(dataset=dataset_instance)
    
    if not equipment_list.exists():
        return {}
    
    flowrates = [e.flowrate for e in equipment_list if e.flowrate is not None]
    pressures = [e.pressure for e in equipment_list if e.pressure is not None]
    temperatures = [e.temperature for e in equipment_list if e.temperature is not None]
    
    # Equipment type distribution
    type_distribution = {}
    for equipment in equipment_list:
        type_distribution[equipment.equipment_type] = type_distribution.get(equipment.equipment_type, 0) + 1
    
    stats = {
        'total_equipment': equipment_list.count(),
        'avg_flowrate': round(sum(flowrates) / len(flowrates), 2) if flowrates else 0,
        'avg_pressure': round(sum(pressures) / len(pressures), 2) if pressures else 0,
        'avg_temperature': round(sum(temperatures) / len(temperatures), 2) if temperatures else 0,
        'equipment_type_distribution': type_distribution,
        'min_flowrate': round(min(flowrates), 2) if flowrates else None,
        'max_flowrate': round(max(flowrates), 2) if flowrates else None,
        'min_pressure': round(min(pressures), 2) if pressures else None,
        'max_pressure': round(max(pressures), 2) if pressures else None,
        'min_temperature': round(min(temperatures), 2) if temperatures else None,
        'max_temperature': round(max(temperatures), 2) if temperatures else None,
    }
    
    return stats


def get_user_summary(user):
    """
    Get summary statistics for all datasets of a user
    """
    datasets = Dataset.objects.filter(user=user).order_by('-uploaded_at')[:5]
    
    all_equipment = Equipment.objects.filter(dataset__user=user)
    
    flowrates = [e.flowrate for e in all_equipment if e.flowrate is not None]
    pressures = [e.pressure for e in all_equipment if e.pressure is not None]
    temperatures = [e.temperature for e in all_equipment if e.temperature is not None]
    
    type_distribution = {}
    for equipment in all_equipment:
        type_distribution[equipment.equipment_type] = type_distribution.get(equipment.equipment_type, 0) + 1
    
    summary = {
        'total_equipment': all_equipment.count(),
        'avg_flowrate': round(sum(flowrates) / len(flowrates), 2) if flowrates else 0,
        'avg_pressure': round(sum(pressures) / len(pressures), 2) if pressures else 0,
        'avg_temperature': round(sum(temperatures) / len(temperatures), 2) if temperatures else 0,
        'equipment_type_distribution': type_distribution,
        'recent_datasets': datasets,
    }
    
    return summary
