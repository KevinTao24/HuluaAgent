from hulua.agents_services.base import BaseAgentService
from hulua.agents_services.mock_agent_service import MockAgentService


def get_agent_service() -> BaseAgentService:
    return MockAgentService()
