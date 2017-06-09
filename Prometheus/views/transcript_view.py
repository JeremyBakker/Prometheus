from rest_framework import viewsets
from Prometheus.serializers.transcript_serializer import TranscriptSerializer
from Prometheus.models import Transcripts


class TranscriptViewSet(viewsets.ModelViewSet):
    
    queryset = Transcripts.objects.all()
    serializer_class = TranscriptSerializer