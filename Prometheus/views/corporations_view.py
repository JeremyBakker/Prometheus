from django.shortcuts import render
from Prometheus.models.transcript_model import Transcripts

def corporations(request):
    
    print("HERE")

    template_name = 'corporations.html'
    context = {}

    transcripts = Transcripts.objects.get(pk=2)
    context = {"transcripts": transcripts, "corporation": "Apple"}

    return render(request, template_name, context)