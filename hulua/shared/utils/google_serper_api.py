import os
import sys
from typing import Any, Dict, Literal, Optional
from hulua.shared.utils.utils import CitedSnippet, summarize_with_sources

sys.path.insert(0, os.path.dirname(__file__) + "/../../..")
from urllib.parse import quote

import aiohttp
import requests


class GoogleSerperAPISearch:
    """
    Wrapper around the Serper.dev Google Search API.

    You can create a free API key at https://serper.dev.

    To use, you should have the environment variable ``SERPER_API_KEY``
    set with your API key, or pass `serper_api_key` as a named parameter
    to the constructor.

    Example:
        .. code-block:: python

            from hulua.shared.utils import GoogleSerperAPISearch
            google_serper = GoogleSerperAPISearch(serper_api_key=GOOGLE_SERPER_API_KEY)
    """

    k: int = 10
    hl: str = "zh"

    aiosession: Optional[aiohttp.ClientSession] = None
    type: Literal["news", "search", "places", "images"] = "search"
    result_key_for_type: Dict = {
        "news": "news",
        "places": "places",
        "images": "images",
        "search": "organic",
    }

    def __init__(self, serper_api_key: Optional[str] = None):
        self.serper_api_key = serper_api_key

    def run(self, query: str, model=None, lang="简体中文", goal="", task="", **kwargs) -> Dict:
        """Run query through GoogleSearch and parse result."""
        results = self._google_serper_search_results(
            query, hl=self.hl, num=self.k, **kwargs
        )

        return summarize_with_sources(model, lang, goal, task, self._parse_results(results, query))

    async def a_run(self, query: str, model=None, lang="简体中文", goal="", task="", **kwargs) -> Dict:
        """Run query through GoogleSearch and parse result async."""

        results = await self._async_google_serper_search_results(
            query, hl=self.hl, num=self.k, **kwargs
        )

        return summarize_with_sources(model, lang, goal, task, self._parse_results(results, query))

    def _google_serper_search_results(
        self, search_term: str, search_type: str = "search", **kwargs: Any
    ) -> Dict:
        headers = {
            "X-API-KEY": self.serper_api_key or "",
            "Content-Type": "application/json",
        }
        params = {
            "q": search_term,
            **{key: value for key, value in kwargs.items() if value is not None},
        }
        response = requests.post(
            f"https://google.serper.dev/{search_type}", headers=headers, params=params
        )
        response.raise_for_status()
        search_results = response.json()
        return search_results

    async def _async_google_serper_search_results(
        self, search_term: str, search_type: str = "search", **kwargs: Any
    ) -> Dict:
        headers = {
            "X-API-KEY": self.serper_api_key or "",
            "Content-Type": "application/json",
        }
        url = f"https://google.serper.dev/{search_type}"
        params = {
            "q": search_term,
            **{key: value for key, value in kwargs.items() if value is not None},
        }

        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, params=params, headers=headers, raise_for_status=False
                ) as response:
                    search_results = await response.json()
        else:
            async with self.aiosession.post(
                url, params=params, headers=headers, raise_for_status=True
            ) as response:
                search_results = await response.json()

        return search_results

    def _parse_results(self, results: Dict, query) -> str:
        snippets = []

        if results.get("answerBox"):
            answer_values = []
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                answer_values.append(answer_box.get("answer"))
            elif answer_box.get("snippet"):
                answer_values.append(answer_box.get("snippet").replace("\n", " "))
            elif answer_box.get("snippetHighlighted"):
                answer_values.append(answer_box.get("snippetHighlighted"))

        if results.get("knowledgeGraph"):
            kg = results.get("knowledgeGraph", {})
            title = kg.get("title")
            entity_type = kg.get("type")
            if entity_type:
                snippets.append(f"{title}: {entity_type}.")
            description = kg.get("description")
            if description:
                snippets.append(description)
            for attribute, value in kg.get("attributes", {}).items():
                snippets.append(f"{title} {attribute}: {value}.")

        for result in results[self.result_key_for_type[self.type]][: self.k]:
            if "snippet" in result:
                snippets.append(result["snippet"])
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f"{attribute}: {value}.")

        if len(snippets) == 0:
            return ["No good Google Search Result was found"]

        return snippets


if __name__ == "__main__":
    import asyncio

    from hulua.secret import GOOGLE_SERPER_API_KEY

    google_serper = GoogleSerperAPISearch(serper_api_key=GOOGLE_SERPER_API_KEY)
    print(asyncio.run(google_serper.a_run("上海天气实时查询")))
