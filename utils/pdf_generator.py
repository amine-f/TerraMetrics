from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
import json
import tempfile
import os

def format_number(number):
    """Format number with thousand separators and 2 decimal places"""
    return "{:,.2f}".format(number)

def create_pie_chart(data, title):
    """Create a pie chart for the emission breakdown"""
    drawing = Drawing(400, 200)
    pie = Pie()
    pie.x = 150
    pie.y = 50
    pie.width = 100
    pie.height = 100
    pie.data = [float(v) for v in data.values()]
    pie.labels = list(data.keys())
    pie.slices.strokeWidth = 0.5
    drawing.add(pie)
    return drawing

def generate_pdf_report(footprint, filename):
    """Generate a detailed PDF report for carbon footprint data"""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    heading2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Custom style for centered text
    centered_style = ParagraphStyle(
        'centered',
        parent=styles['Normal'],
        alignment=1,
        spaceAfter=30
    )
    
    # Build the document
    elements = []
    
    # Title
    elements.append(Paragraph("Carbon Footprint Report By WELINK TECH", title_style))
    elements.append(Paragraph(
        f"Generated on {datetime.fromtimestamp(footprint.created_at).strftime('%Y-%m-%d %H:%M:%S')}",
        centered_style
    ))
    elements.append(Spacer(1, 20))
    
    # Summary Table
    summary_data = [
        ["Category", "Emissions (kgCO₂e)"],
        ["Scope 1 (Direct)", format_number(footprint.scope1_emissions)],
        ["Scope 2 (Energy)", format_number(footprint.scope2_emissions)],
        ["Scope 3 (Indirect)", format_number(footprint.scope3_emissions)],
        ["Total Emissions", format_number(footprint.total_emissions)],
        ["Total (Metric Tons)", format_number(footprint.total_emissions/1000)]
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 30))
    
    # Detailed Breakdown
    elements.append(Paragraph("Detailed Emissions Breakdown", heading2_style))
    elements.append(Spacer(1, 20))
    
    # Get emission details
    details = footprint.emission_details
    
    # Scope 1 Breakdown
    elements.append(Paragraph("Scope 1 - Direct Emissions", heading2_style))
    scope1_data = [
        ["Source", "Emissions (kgCO₂e)"]
    ] + [[k.title(), format_number(v)] for k, v in details['scope1'].items()]
    
    scope1_table = Table(scope1_data, colWidths=[4*inch, 2*inch])
    scope1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(scope1_table)
    elements.append(Spacer(1, 20))
    
    # Scope 2 Breakdown
    elements.append(Paragraph("Scope 2 - Energy Indirect Emissions", heading2_style))
    scope2_data = [
        ["Source", "Emissions (kgCO₂e)"]
    ] + [[k.title(), format_number(v)] for k, v in details['scope2'].items()]
    
    scope2_table = Table(scope2_data, colWidths=[4*inch, 2*inch])
    scope2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(scope2_table)
    elements.append(Spacer(1, 20))
    
    # Scope 3 Breakdown
    elements.append(Paragraph("Scope 3 - Other Indirect Emissions", heading2_style))
    scope3_data = [
        ["Source", "Emissions (kgCO₂e)"]
    ] + [[k.title().replace('_', ' '), format_number(v)] for k, v in details['scope3'].items()]
    
    scope3_table = Table(scope3_data, colWidths=[4*inch, 2*inch])
    scope3_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(scope3_table)
    elements.append(Spacer(1, 20))
    
    # Recommendations
    elements.append(Paragraph("Recommendations for Reduction", heading2_style))
    recommendations = [
        "Consider transitioning to renewable energy sources to reduce Scope 2 emissions",
        "Implement energy efficiency measures in facilities",
        "Optimize transportation routes and consider electric vehicles",
        "Engage suppliers in sustainability initiatives",
        "Implement waste reduction and recycling programs"
    ]
    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", normal_style))
        elements.append(Spacer(1, 10))
    
    # Build PDF
    doc.build(elements)
    
def get_report_download_link(footprint):
    """Generate a PDF report and return it as a base64 string"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        generate_pdf_report(footprint, tmp.name)
        with open(tmp.name, 'rb') as f:
            pdf_data = f.read()
        os.unlink(tmp.name)
        return pdf_data
