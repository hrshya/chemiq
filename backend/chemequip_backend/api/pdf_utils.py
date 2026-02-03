"""
PDF generation utilities
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from io import BytesIO
from django.core.files.base import ContentFile
from chemequip_backend.api.models import Dataset
from datetime import datetime


def generate_pdf_report(dataset_id, user):
    """
    Generate a PDF report for a dataset
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=user)
    except Dataset.DoesNotExist:
        return None, "Dataset not found"
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
    )
    
    # Title
    elements.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Dataset Information
    elements.append(Paragraph("Dataset Information", heading_style))
    info_data = [
        ['Filename:', dataset.filename],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Equipment:', str(dataset.equipment_count)],
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8EEF7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    stats = dataset.summary_stats
    
    stats_data = [
        ['Metric', 'Value'],
        ['Average Flowrate (L/min):', f"{stats.get('avg_flowrate', 'N/A')}"],
        ['Average Pressure (Bar):', f"{stats.get('avg_pressure', 'N/A')}"],
        ['Average Temperature (°C):', f"{stats.get('avg_temperature', 'N/A')}"],
        ['Min Flowrate:', f"{stats.get('min_flowrate', 'N/A')}"],
        ['Max Flowrate:', f"{stats.get('max_flowrate', 'N/A')}"],
        ['Min Pressure:', f"{stats.get('min_pressure', 'N/A')}"],
        ['Max Pressure:', f"{stats.get('max_pressure', 'N/A')}"],
        ['Min Temperature:', f"{stats.get('min_temperature', 'N/A')}"],
        ['Max Temperature:', f"{stats.get('max_temperature', 'N/A')}"],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F4F8')]),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    elements.append(Paragraph("Equipment Type Distribution", heading_style))
    type_dist = stats.get('equipment_type_distribution', {})
    dist_data = [['Equipment Type', 'Count']]
    for equip_type, count in type_dist.items():
        dist_data.append([equip_type, str(count)])
    
    dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F4F8')]),
    ]))
    elements.append(dist_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment Details
    elements.append(PageBreak())
    elements.append(Paragraph("Equipment Details", heading_style))
    
    equipment_list = dataset.equipment.all()
    equip_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
    for equip in equipment_list:
        equip_data.append([
            equip.name,
            equip.equipment_type,
            f"{equip.flowrate}" if equip.flowrate else 'N/A',
            f"{equip.pressure}" if equip.pressure else 'N/A',
            f"{equip.temperature}" if equip.temperature else 'N/A',
        ])
    
    equip_table = Table(equip_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    equip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F4F8')]),
    ]))
    elements.append(equip_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer, "PDF generated successfully"
