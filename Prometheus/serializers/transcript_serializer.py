"""
bangazon api serializer configuration for computer
"""

from rest_framework import serializers
from Prometheus.models.transcript_model import Transcripts


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Transcripts
        exclude = ()