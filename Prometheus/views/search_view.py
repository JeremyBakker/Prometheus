from django.shortcuts import render
from django.apps import apps
import datetime


def search (request):
    try:
        transcript = request.GET['transcript']
        corporation = transcript.split("-")[0]
        transcript_date = transcript.split("-")[1]

        transcript_date_for_db = datetime.datetime.strptime((transcript_date), "%d %B %y")
        transcript_date_for_db = datetime.datetime.strftime((transcript_date_for_db), "%Y-%m-%d")

        model = apps.get_model('Prometheus', corporation)

        answers_query_set = model.objects.filter(date_of_call = transcript_date_for_db, question=0)
        print("transcript_date_for_db", transcript_date_for_db)
        print("answers_query_set", answers_query_set)
        print("length", len(answers_query_set))

        for answer in answers_query_set:
            print(answer.name)

    except KeyError:
        corporation = ""
        pass

    template = 'index.html'
    context = {"search_view": True, "corporation": corporation}
    return render(request, template, context)
