import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import EquipmentDataset
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            # Read the CSV using Pandas
            df = pd.read_csv(file_obj)
            
            # Ensure required columns exist, handling Flowrate specifically
            flowrate_mean = df['Flowrate'].mean() if 'Flowrate' in df.columns else 0
            pressure_mean = df['Pressure'].mean() if 'Pressure' in df.columns else 0
            temp_mean = df['Temperature'].mean() if 'Temperature' in df.columns else 0

            # Generate the summary object
            summary = {
                "total_count": len(df),
                "avg_pressure": float(pressure_mean),
                "avg_temperature": float(temp_mean),
                "avg_flowrate": float(flowrate_mean),
                "type_distribution": df['Type'].value_counts().to_dict() if 'Type' in df.columns else {}
            }

            # --- HISTORY MANAGEMENT LOGIC ---
            # 1. Save this upload to the database
            EquipmentDataset.objects.create(
                file_name=file_obj.name, 
                summary_data=summary
            )

            # 2. Keep only the last 5 uploads (Delete older ones)
            if EquipmentDataset.objects.count() > 5:
                ids_to_keep = EquipmentDataset.objects.order_by('-uploaded_at')[:5].values_list('id', flat=True)
                EquipmentDataset.objects.exclude(id__in=ids_to_keep).delete()
            # --------------------------------

            return Response({
                "summary": summary, 
                "data": df.to_dict(orient='records')
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class HistoryView(APIView):
    def get(self, request):
        # Fetch last 5 records for the frontend history list
        history = EquipmentDataset.objects.all().order_by('-uploaded_at')
        data = [
            {
                "id":h.id,
                "file": h.file_name, 
                "date": h.uploaded_at, 
                "summary": h.summary_data
            } for h in history
        ]
        return Response(data)

def download_pdf_report(request,report_id):
    record = get_object_or_404(EquipmentDataset, id=report_id)
    summary = record.summary_data
    # This generates the PDF for the download buttons
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Report_{record.file_name}.pdf"'
    
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f" Analytics Report:{record.file_name}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 775, f"Date: {record.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
    p.line(100, 765, 500, 765)
    
   # Draw the specific data stored in summary_data
    p.drawString(100, 740, f"Total Items: {summary.get('total_count')}")
    p.drawString(100, 720, f"Average Pressure: {summary.get('avg_pressure'):.2f} PSI")
    p.drawString(100, 700, f"Average Temperature: {summary.get('avg_temperature'):.2f} °C")
    p.drawString(100, 680, f"Average Flowrate: {summary.get('avg_flowrate'):.2f} m³/h")
    p.showPage()
    p.save()
    return response