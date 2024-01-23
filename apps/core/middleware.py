from django.contrib.sessions.middleware import SessionMiddleware


class XOSessionMiddleware(SessionMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)

        self.session_objects = {
            "search_query": "",
            "search_results": {},
            "provider": "",
            "data": {
                "details": {},
                "feed": [],
                "id": "",
                "item": {},
                "items": [],
                "links": {},
                "movies": {},
                "now_playing": "",
                "popular": {},
                "recent": {},
                "top": {},
                "type": "",
            },
            "previous": {},
            "next": {},
        }

    def __call__(self, request):
        for key, value in self.session_objects.items():
            if key not in request.session:
                self.fetch_data(request, key, value)

        # Search Query
        request.get_search_query = lambda: self.get_session_value(
            request, "search_query"
        )
        request.set_search_query = lambda value: self.set_session_value(
            request, "search_query", value
        )

        # Search Results
        request.get_search_results = lambda: self.get_session_value(
            request, "search_results"
        )
        request.set_search_results = lambda value: self.set_session_value(
            request, "search_results", value
        )

        # Search Provider
        request.get_provider = lambda: self.get_session_value(request, "provider")
        request.set_provider = lambda value: self.set_session_value(
            request, "provider", value
        )

        # ID
        request.get_id = lambda: self.get_data(request, "id")
        request.set_id = lambda value: self.set_data(request, "id", value)

        # Details
        request.get_details = lambda: self.get_data(request, "details")
        request.set_details = lambda value: self.set_data(request, "details", value)

        # Items
        request.get_items = lambda: self.get_data(request, "items")
        request.set_items = lambda value: self.set_data(request, "items", value)

        # Item
        request.get_item = lambda: self.get_data(request, "item")
        request.set_item = lambda value: self.set_data(request, "item", value)

        # Now Playing
        request.get_now_playing = lambda: self.get_data(request, "now_playing")
        request.set_now_playing = lambda value: self.set_data(
            request, "now_playing", value
        )

        # Links
        request.get_links = lambda: self.get_data(request, "links")
        request.set_links = lambda value: self.set_data(request, "links", value)

        # Previous
        request.get_previous = lambda: self.get_session_value(request, "previous")
        request.set_previous = lambda value: self.set_session_value(
            request, "previous", value
        )

        # Next
        request.get_next = lambda: self.get_session_value(request, "next")
        request.set_next = lambda value: self.set_session_value(request, "next", value)

        # News Feed
        request.get_news_feed = lambda: self.get_data(request, "feed")
        request.set_news_feed = lambda value: self.set_data(request, "feed", value)

        # Recent
        request.get_recent = lambda: self.get_data(request, "recent")
        request.set_recent = lambda value: self.set_data(request, "recent", value)

        # Top
        request.get_top = lambda: self.get_data(request, "top")
        request.set_top = lambda value: self.set_data(request, "top", value)

        # Popular
        request.get_popular = lambda: self.get_data(request, "popular")
        request.set_popular = lambda value: self.set_data(request, "popular", value)

        # Movies
        request.get_movies = lambda: self.get_data(request, "movies")
        request.set_movies = lambda value: self.set_data(request, "movies", value)

        # Type
        request.get_type = lambda: self.get_data(request, "type")
        request.set_type = lambda value: self.set_data(request, "type", value)

        return super().__call__(request)

    def fetch_data(self, request, key, value):
        if key in self.session_objects:
            request.session[key] = value

    def get_session_value(self, request, key):
        return request.session.get(key, None)

    def set_session_value(self, request, key, value):
        request.session[key] = value

    def get_data(self, request, key):
        data = request.session.get("data", {})
        return data.get(key, None)

    def set_data(self, request, key, value):
        data = request.session.get("data", {})
        data[key] = value
        request.session["data"] = data
