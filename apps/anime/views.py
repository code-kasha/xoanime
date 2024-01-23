from django.contrib import messages

from django.shortcuts import render, redirect

from django.views.generic import View

from apps.utils.helpers.fetch import fetch

BASE_URL = "http://localhost:3000/anime/"


class SearchView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return (
            request.GET.get("query"),
            int(request.GET.get("page", 1)),
        )

    def get_result(self, request):
        return (
            request.get_search_query(),
            request.get_search_results(),
        )

    def process(self, request, query, page):
        url = f"{BASE_URL}{query}?page={page}"

        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, query, results)
        else:
            self.set_result(request, "", {})

    def set_result(self, request, query, results):
        request.set_search_query(query)
        request.set_search_results(results)

    def get(self, request):
        query, page = self.get_attrs(request)
        search_query, search_results = self.get_result(request)

        if (
            not search_results
            or search_query != query
            or page != self.get_current_page(search_results)
        ):
            self.process(request, query, page)

        if not request.get_search_results or not request.get_search_query:
            return redirect(to="index")

        return render(request, "anime/search.html")


search = SearchView.as_view()


class DetailsView(View):
    def get_attrs(self, request):
        return request.GET.get("id"), request.GET.get("episodeId")

    def get_result(self, request):
        return request.get_id(), request.get_details()

    def process(self, request, details, id, episodeId=None):
        _id = details.pop("id", "")
        item_id = id if id else _id

        if "episodes" in details:
            items = details.pop("episodes", [])
            items = [item for item in items if item.get("id")]
            items = sorted(items, key=lambda x: x.get("number", ""))

        item = items[0] if items else {}

        now_playing = episodeId if episodeId else item.get("id", "")

        self.set_result(request, item_id, details, items, item, now_playing)

    def set_result(self, request, id, details, items, item, now_playing):
        request.set_id(id)
        request.set_details(details)
        request.set_items(items)
        request.set_item(item)
        request.set_now_playing(now_playing)
        request.set_links({})

    def get(self, request):
        id, episodeId = self.get_attrs(request)
        item_id, item_details = self.get_result(request)

        if not item_details or item_id != id:
            url = f"{BASE_URL}info/{id}"
            details = fetch(request, url)

            if details:
                self.process(request, details, id, episodeId)
                if episodeId:
                    return redirect("anime:watch")
            else:
                self.set_result(request, "", {}, [], {}, "")
                return redirect(to="index")

        return render(request, "anime/details.html")


details = DetailsView.as_view()


class WatchView(View):
    def get_attrs(self, request):
        return request.GET.get("id")

    def get_context(self, request):
        items = request.get_items()
        now_playing = request.get_now_playing()

        current_episode = next(
            (index for index, item in enumerate(items) if item["id"] == now_playing),
            None,
        )

        previous_episode = (
            items[current_episode - 1]
            if items and current_episode is not None and current_episode > 0 and items
            else None
        )

        next_episode = (
            items[current_episode + 1]
            if items
            and current_episode is not None
            and current_episode < len(items) - 1
            and items
            else None
        )

        request.set_next(next_episode)
        request.set_previous(previous_episode)

    def get_data(self, request):
        return request.get_now_playing()

    def get_links(self, request):
        now_playing = self.get_data(request)

        url = f"{BASE_URL}watch/{now_playing}"

        links = fetch(request, url)

        if links is not None and links:
            request.set_links(links)
        else:
            request.set_links({})

        self.get_context(request)

    def get(self, request):
        id = self.get_attrs(request)

        items = request.get_items()
        links = request.get_links()
        now_playing = request.get_now_playing()

        if items and not links:
            self.get_links(request)

        elif id != now_playing and items:
            current = next(
                (item for item in items if item["id"] == id),
                None,
            )
            if current:
                request.set_item(current)
                request.set_now_playing(current.get("id", ""))

                if request.get_item() and request.get_now_playing():
                    self.get_links(request)

        if not request.get_links():
            return redirect(to="index")

        return render(request, f"anime/watch.html")


watch = WatchView.as_view()


class GenreView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return (
            request.GET.get("slug"),
            int(request.GET.get("page", 1)),
        )

    def get_result(self, request):
        return (
            request.get_search_query(),
            request.get_search_results(),
        )

    def process(self, request, slug, page):
        url = f"{BASE_URL}genre/{slug}?page={page}"

        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, slug, results)
        else:
            self.set_result(request, "", {})

    def set_result(self, request, slug, results):
        request.set_search_query(slug)
        request.set_search_results(results)

    def get(self, request):
        slug, page = self.get_attrs(request)
        search_query, search_results = self.get_result(request)

        if (
            not search_results
            or search_query != slug
            or page != self.get_current_page(search_results)
        ):
            self.process(request, slug, page)

        if not request.get_search_results or not request.get_search_query:
            return redirect(to="index")

        request.set_provider("anime")
        return render(request, "anime/genre.html")


genre = GenreView.as_view()


class TopAiringView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return int(request.GET.get("page", 1))

    def get_result(self, request):
        return request.get_top()

    def process(self, request, page):
        url = f"{BASE_URL}top-airing?page={page}"
        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, results)
        else:
            self.set_result(request, {})

    def set_result(self, request, results):
        request.set_top(results)
        request.set_provider("anime")

    def get(self, request):
        page = self.get_attrs(request)
        results = self.get_result(request)

        current_page = self.get_current_page(results)

        if not results or page != current_page:
            self.process(request, page)

        if not request.get_top():
            return redirect(to="index")

        return render(request, "anime/top.html")


top = TopAiringView.as_view()


class MoviesView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return int(request.GET.get("page", 1))

    def get_result(self, request):
        return request.get_movies()

    def process(self, request, page):
        url = f"{BASE_URL}movies?page={page}"
        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, results)
        else:
            self.set_result(request, {})

    def set_result(self, request, results):
        request.set_movies(results)

    def get(self, request):
        page = self.get_attrs(request)
        results = self.get_result(request)

        current_page = self.get_current_page(results)

        if not results or page != current_page:
            self.process(request, page)

        if not request.get_movies():
            return redirect(to="index")

        request.set_provider("anime")
        return render(request, "anime/movies.html")


movies = MoviesView.as_view()


class PopularView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return int(request.GET.get("page", 1))

    def get_result(self, request):
        return request.get_popular()

    def process(self, request, page):
        url = f"{BASE_URL}popular?page={page}"
        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, results)
        else:
            self.set_result(request, {})

    def set_result(self, request, results):
        request.set_popular(results)

    def get(self, request):
        page = self.get_attrs(request)
        results = self.get_result(request)

        current_page = self.get_current_page(results)

        if not results or page != current_page:
            self.process(request, page)

        if not request.get_popular():
            return redirect(to="index")

        request.set_provider("anime")
        return render(request, "anime/popular.html")


popular = PopularView.as_view()


class RecentEpisodesView(View):
    def get_current_page(self, results):
        return int(results.get("currentPage")) if results else int(1)

    def get_attrs(self, request):
        return int(request.GET.get("page", 1)), int(request.GET.get("type", 1))

    def get_result(self, request):
        return request.get_recent(), request.get_type()

    def process(self, request, page, type):
        url = f"{BASE_URL}recent-episodes?page={page}&type={type}"
        results = fetch(request, url)

        if results and results is not None:
            self.set_result(request, results, type)
        else:
            self.set_result(request, {}, "")

    def set_result(self, request, results, type):
        request.set_recent(results)
        request.set_type(type)

    def get(self, request):
        page, type = self.get_attrs(request)

        results, audio_type = self.get_result(request)

        current_page = self.get_current_page(results)

        if not results or page != current_page or audio_type != type:
            self.process(request, page, type)

        if not request.get_recent():
            return redirect(to="index")

        request.set_provider("anime")
        return render(request, "anime/recent.html")


recent = RecentEpisodesView.as_view()
