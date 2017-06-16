from django.shortcuts import render


def index(request):
    '''
    This function renders the index view, which shows the Dow Jones Industrial 
    Average on the D3 line graph as well as all relevant navigation 
    affordances.

    ---Arguments---
    request: the full HTTP request object

    ---Return Value---
    request: the full HTTP request object
    template: index.html
    context: "corporation": None
    '''

    template_name = 'index.html'
    context = {"corporation": None}

    return render(request, template_name, context)