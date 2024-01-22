from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


def clear(request):
    request.session.flush()
    return redirect("index")
