import unittest
from services.agent_manager import AgentManager


class TestAgentManager(unittest.TestCase):
    def setUp(self):
        self.agent_manager = AgentManager()
    
    def test_add_agent(self):
        role = "22-year-old CS student"
        self.agent_manager.add_agent(role)
        self.assertEqual(self.agent_manager.list_of_agents[0].role, "22-year-old CS student")
