from django.shortcuts import render


def search (request):
    print(request.path)
    template = 'index.html'

    transcript = request.GET['transcript']
    corporation = transcript.split("-")[0]
    print("transcript corporation", corporation)
    print("type", type(corporation))

    context = {"test": "TESSSSSSSSST", "corporation": corporation}
    print("transcript", transcript)

    return render(request, template, context)