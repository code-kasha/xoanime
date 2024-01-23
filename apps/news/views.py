from django.contrib import messages

from django.shortcuts import render, redirect

from django.views.generic import View

from apps.utils.helpers.fetch import fetch

BASE_URL = "http://localhost:3000/news/"


class FeedView(View):
    def get(self, request):
        url = BASE_URL + "recent-feeds"

        news_feed = request.get_news_feed()

        if not news_feed:
            result = fetch(request, url)
            if result:
                request.set_news_feed(result)
                messages.success(request, "News Feed Fetched.")
            else:
                messages.error(request, "Could not get feed.")
        return redirect("index")


feed = FeedView.as_view()


class FeedDetails(View):
    def get(self, request):
        id = request.GET.get("id")

        url = BASE_URL + f"info?id={id}"

        result = fetch(request, url)
        if result:
            return render(request, "news/article.html", {"data": result})
        else:
            messages.error(request, "Could not get article.")

        return redirect("index")


details = FeedDetails.as_view()
