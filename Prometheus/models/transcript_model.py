from django.db import models


class Transcripts (models.Model):

    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    question_answer_text = models.CharField(max_length=1000)
    question = models.BooleanField()
    date_of_call = models.CharField(max_length=10)