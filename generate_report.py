import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

# 1. Read and analyze data
def analyze_data(file_path):
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Basic analysis
    total_sales = df['Units Sold'].sum()
    total_revenue = df['Revenue'].sum()
    avg_revenue_per_sale = total_revenue / total_sales
    top_product = df.groupby('Product')['Revenue'].sum().idxmax()
    
    return df, {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'avg_revenue_per_sale': avg_revenue_per_sale,
        'top_product': top_product
    }

# 2. Create a chart
def create_chart(df):
    plt.figure(figsize=(8, 4))
    for product in df['Product'].unique():
        product_data = df[df['Product'] == product]
        plt.plot(product_data['Date'], product_data['Revenue'], marker='o', label=product)
    plt.title('Daily Revenue by Product')
    plt.xlabel('Date')
    plt.ylabel('Revenue ($)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save to BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()
    return buffer

# 3. Generate PDF report
def generate_pdf_report(df, analysis, chart_buffer, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph("Sales Report - April 2025", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Summary
    summary_text = f"""
    <b>Total Units Sold:</b> {analysis['total_sales']}<br/>
    <b>Total Revenue:</b> ${analysis['total_revenue']:,.2f}<br/>
    <b>Average Revenue per Sale:</b> ${analysis['avg_revenue_per_sale']:,.2f}<br/>
    <b>Top Product:</b> {analysis['top_product']}
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Data Table
    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    story.append(Paragraph("Sales Data", styles['Heading2']))
    story.append(table)
    story.append(Spacer(1, 12))
    
    # Chart
    chart_image = Image(chart_buffer, width=400, height=200)
    story.append(Paragraph("Revenue Trend", styles['Heading2']))
    story.append(chart_image)
    
    # Build PDF
    doc.build(story)
    chart_buffer.close()

# Main execution
def main():
    file_path = "sales_data.csv"
    output_file = "sales_report.pdf"
    
    # Analyze data
    df, analysis = analyze_data(file_path)
    
    # Create chart
    chart_buffer = create_chart(df)
    
    # Generate report
    generate_pdf_report(df, analysis, chart_buffer, output_file)
    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    main()