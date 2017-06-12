from django.shortcuts import render


def search (request):
    print(request.path)
    template = 'index.html'
    try:
        transcript = request.GET['transcript']
        corporation = transcript.split("-")[0]
    except KeyError:
        corporation = ""
        pass

    context = {"search_view": True, "corporation": corporation}
    return render(request, template, context)
