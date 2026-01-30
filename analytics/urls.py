from django.urls import path
from .views import CSVUploadView, HistoryView, download_pdf_report

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('report/<int:report_id>/', download_pdf_report, name='pdf-report'),
]