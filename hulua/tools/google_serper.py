import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(__file__) + "/../..")
from hulua.secret import GOOGLE_SERPER_API_KEY
from hulua.shared.utils.google_serper_api import GoogleSerperAPISearch
from hulua.tools.tool import Tool


class GoogleSerperTool(Tool):
    name: str = "search"
    description: str = "Search the internet using Google Serper API"
    serper_api_search: Optional[GoogleSerperAPISearch] = GoogleSerperAPISearch(
        serper_api_key=GOOGLE_SERPER_API_KEY
    )

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
        results = self.serper_api_search.run(
            query=input, model=self.model, goal=goal, task=task, **kwargs
        )

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

        results = await self.serper_api_search.a_run(
            query=input, model=self.model, goal=goal, task=task, **kwargs
        )

        return results


if __name__ == "__main__":
    import asyncio

    from hulua.secret import GOOGLE_SERPER_API_KEY

    google_serper_tool = GoogleSerperTool()
    google_serper_api_search = GoogleSerperAPISearch(
        serper_api_key=GOOGLE_SERPER_API_KEY
    )
    google_serper_tool.serper_api_search = google_serper_api_search

    print(asyncio.run(google_serper_tool.a_call(input="上海天气实时查询")))
