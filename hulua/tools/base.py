from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str = ""  # tool name
    icon: str = ""  # tool icon
    type: str = ""  # tool type
    category: str = ""  # tool category
    description: str = ""  # tool description

    @abstractmethod
    def call(
        self, goal: str, task: str, input: str, user_id: str, *args, **kwargs
    ) -> dict:
        pass

    @abstractmethod
    async def a_call(
        self, goal: str, task: str, input: str, user_id: str, *args, **kwargs
    ) -> dict:
        pass
