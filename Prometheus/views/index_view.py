from django.shortcuts import render
from Prometheus.models.transcript_model import Transcripts

def index(request):
    
    template_name = 'index.html'
    context = {}

    transcripts = Transcripts.objects.get(pk=1)
    context = {"transcripts": transcripts}

    return render(request, template_name, context)