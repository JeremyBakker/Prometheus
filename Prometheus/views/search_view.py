def search (request):
    print(request.path)
    template = 'corporations.html'
    context = {}

    return render(request, template, context)