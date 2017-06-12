from django.shortcuts import render


def search (request):
    print(request.path)
    template = 'corporations.html'
    context = {}

    return render(request, template, context)