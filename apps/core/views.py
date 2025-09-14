from django.shortcuts import render

def index(request):
    """
    This view renders the main home page of the site.
    """
    return render(request, "index.html")

