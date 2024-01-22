from django.contrib import messages
from django.views.generic import View

from django.shortcuts import render, redirect

from apps.utils.helpers.fetch import fetch

BASE_URL = "http://localhost:3000/light-novels/readlightnovels/"


class SearchView(View):
    """
    Performs search for light novels.

    Attributes:
        query (str): The search query entered by the user.

    Methods:
        get_results(request):
            Retrieve stored search results, query, and provider from the session.

        set_results(request, query, results):
            Store the search query and results in the session.

        process(request, query):
            Handle the search operation.

        get(request):
            Handle GET requests for the search view.
    """

    def get_results(self, request):
        """
        Retrieve stored search results, query, and provider from the session.

        Args:
            request (HttpRequest): The HTTP request object containing search-related information.

        Returns:
            tuple: A tuple containing the search query (str), search results (object), and search provider (str).
        """
        return (
            request.get_search_query(),
            request.get_search_results(),
        )

    def set_results(self, request, query, results):
        """
        Store the provided search query and results in the session.

        Args:
            request (HttpRequest): The HTTP request object to store search-related information.
            query (str): The search query to be stored.
            results: The search results to be stored.
        """
        if query and results:
            request.set_search_query(query)
            request.set_search_results(results)
        else:
            request.set_search_query("")
            request.set_search_results({})

    def process(self, request, query):
        """
        Perform a search operation using the provided query and update the search results in the request object.

        Args:
            request (HttpRequest): The HTTP request object containing search-related information.
            query (str): The Search Query

        Returns:
            HttpResponse: A response object based on the search results or an error redirection.
        """
        url = BASE_URL + f"{query}"
        results = fetch(request, url)
        if results is not None:
            self.set_results(request, query, results)
        else:
            messages.error(request, "No results found.")
            return redirect("index")

    def get(self, request):
        """
        Handle GET requests for the search view.

        Args:
            request (HttpRequest): The HTTP request object containing search-related information.

        Returns:
            HttpResponse: A response object rendering the 'novels/search.html' template.
        """
        query = request.GET.get("query")
        search_query, search_results = self.get_results(request)

        if not search_results or search_query != query:
            self.process(request, query)

        return render(request, "novels/search.html")


search = SearchView.as_view()


class DetailsView(View):
    """
    View for displaying details of a web novel.

    Methods:
        get_details(request):
            Retrieve item details, item ID, and provider from the session and ID from the request.

        set_details(request, result, id, items, item, item_id):
            Set various details in the request object.

        process(request):
            Fetch details for the item from an external source and update the request object.

        get(request):
            Handle GET requests for displaying item details.
    """

    def get_details(self, request):
        """
        Retrieve item details, item ID, and provider from the session.

        Args:
            request (HttpRequest): The HTTP request object containing item-related information.

        Returns:
            tuple: A tuple containing the ID (str), item ID (str), item details (object), and item provider (str).
        """
        return (
            request.GET.get("id"),
            request.get_id(),
            request.get_details(),
        )

    def set_details(self, request, result, id, items, item, item_id):
        """
        Set various details in the request object.

        Args:
            request (HttpRequest): The HTTP request object to update.
            result (dict): The result obtained from external data.
            id (str): The item ID.
            items (list): List of chapters related to the novel.
            item (dict): The current chapter.
            item_id (str): The ID of the current chapter.
        """
        request.set_id(id)
        request.set_items(items)
        request.set_item(item)
        request.set_details(result)
        request.set_now_playing(item_id)

    def process(self, request, id):
        """
        Fetch details for the item from an external source and update the request object.

        Args:
            request (HttpRequest): The HTTP request object containing item-related information.
        """
        url = BASE_URL + f"info?id={id}"
        result = fetch(request, url)

        if result:
            id = result.pop("id", "")
            items = [item for item in result.get("chapters", []) if item.get("id")]
            item = items[0] if items else {}
            item_id = item.get("id", "")

            self.set_details(request, result, id, items, item, item_id)

        else:
            self.set_details(request, {}, "", [], {}, "")

    def get(self, request):
        """
        Handle GET requests for displaying item details.

        Args:
            request (HttpRequest): The HTTP request object containing item-related information.

        Returns:
            HttpResponse: A response object rendering the 'novels/details.html' template.
        """

        id, item_id, details = self.get_details(request)

        if not details or item_id != id:
            self.process(request, id)

        return render(request, "novels/details.html")


details = DetailsView.as_view()


class ReadView(View):
    """
    View for reading chapters of a light novel.

    Methods:
        get_data(request):
            Retrieve relevant data from the request, including the chapter ID, items, now playing chapter, and links.

        process(request, id, items):
            Process the chapter request, fetching the chapter content and updating request attributes accordingly.

        get(request):
            Handle GET requests for reading chapters and render the 'novels/read.html' template.
    """

    def get_data(self, request):
        """
        Retrieve relevant data from the request.

        Args:
            request (HttpRequest): The HTTP request object containing chapter-related information.

        Returns:
            tuple: A tuple containing the chapter ID (str), items (list), now playing chapter (str), and links (dict).
        """
        return (
            request.GET.get("id"),
            request.get_items(),
            request.get_now_playing(),
            request.get_links(),
        )

    def process(self, request, id, items):
        """
        Process the chapter request, fetching the chapter content and updating request attributes accordingly.

        Args:
            request (HttpRequest): The HTTP request object containing chapter-related information.
            id (str): The ID of the requested chapter.
            items (list): List of available chapters.
        """
        url = BASE_URL + f"read?chapterId={id}"

        current = next(
            (item for item in items if item["id"] == id),
            None,
        )

        if current:
            request.set_now_playing(current.get("id", ""))
            result = fetch(request, url)
            if result:
                request.set_links(result)
            else:
                request.set_links({})

            current_ep = None
            for index, item in enumerate(items):
                if item["id"] == current["id"]:
                    current_ep = index
                    break

            previous_ep = (
                items[current_ep - 1]
                if current_ep is not None and current_ep > 0
                else None
            )

            next_ep = (
                items[current_ep + 1]
                if current_ep is not None and current_ep < len(items) - 1
                else None
            )

            request.set_previous(previous_ep)
            request.set_next(next_ep)

    def get(self, request):
        """
        Handle GET requests for reading chapters and render the 'novels/read.html' template.

        Args:
            request (HttpRequest): The HTTP request object containing chapter-related information.

        Returns:
            HttpResponse: A response object rendering the 'novels/read.html' template.
        """
        id, items, now_playing, links = self.get_data(request)

        if items and (not links or id != now_playing):
            self.process(request, id, items)

        return render(request, "novels/read.html")


read = ReadView.as_view()
