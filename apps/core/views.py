from django.shortcuts import render, redirect

from django.urls import reverse


def index(request):
    return render(request, "index.html")


def clear(request):
    request.session.flush()
    return redirect("index")


def search(request):
    query = request.GET.get("query")
    provider = request.GET.get("provider")

    search_query = request.get_search_query()
    search_provider = request.get_provider()

    if query != search_query or search_provider != provider:
        request.set_search_query("")
        request.set_search_results({})
        request.set_provider(provider)

    url = reverse(f"{provider}:search") + f"?query={query}"
    return redirect(url)
