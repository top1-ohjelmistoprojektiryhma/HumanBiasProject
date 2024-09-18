import unittest
from backend.services.agent_manager import AgentManager


class ExampleAgent:
    def __init__(self, role):
        self.role = role


class TestAgentManager(unittest.TestCase):
    def setUp(self):
        self.agent_manager = AgentManager()

    def test_add_agent(self):
        role = "22-year-old CS student"
        self.agent_manager.add_agent(role)
        self.assertEqual(
            self.agent_manager.list_of_agents[0].role, "22-year-old CS student"
        )

    def test_delete_agent(self):
        self.agent_manager.list_of_agents = [
            ExampleAgent("22-year-old CS student"),
            ExampleAgent("CS Professor"),
        ]
        self.agent_manager.delete_agent("22-year-old CS student")
        self.assertEqual(self.agent_manager.list_of_agents[0].role, "CS Professor")

    def test_set_selected_agents(self):
        self.agent_manager.list_of_agents = [
            ExampleAgent("22-year-old CS student"),
            ExampleAgent("CS Professor"),
        ]
        self.agent_manager.set_selected_agents(
            ["22-year-old CS student", "CS Professor"]
        )
        self.assertEqual(
            self.agent_manager.selected_agents[0].role, "22-year-old CS student"
        )
        self.assertEqual(self.agent_manager.selected_agents[1].role, "CS Professor")
