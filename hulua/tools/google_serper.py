from typing import Optional

from hulua.shared.utils.google_serper_api import GoogleSerperAPISearch
from hulua.tools.base import BaseTool


class GoogleSerperTool(BaseTool):
    name: str = "GoogleSerperTool"
    description: str = "Search the internet using Google Serper API"
    serper_api_search: Optional[GoogleSerperAPISearch] = None

    def call(
        self,
        goal: str = "",
        task: str = "",
        input: str = "",
        user_id: str = "",
        *args,
        **kwargs
    ) -> dict:
        """Run query through GoogleSearch and parse result."""
        results = self.serper_api_search.run(input, **kwargs)

        return results

    async def a_call(
        self,
        goal: str = "",
        task: str = "",
        input: str = "",
        user_id: str = "",
        *args,
        **kwargs
    ) -> dict:
        """Run query through GoogleSearch and parse result async."""

        results = await self.serper_api_search.a_run(input, **kwargs)

        return results


if __name__ == "__main__":
    import asyncio

    from hulua.secret import GOOGLE_SERPER_API_KEY

    google_serper_tool = GoogleSerperTool()
    google_serper_api_search = GoogleSerperAPISearch(
        serper_api_key=GOOGLE_SERPER_API_KEY
    )
    google_serper_tool.serper_api_search = google_serper_api_search

    print(asyncio.run(google_serper_tool.a_call(input="中国首都是哪里")))
