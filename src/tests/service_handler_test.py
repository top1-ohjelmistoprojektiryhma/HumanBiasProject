import unittest
from services.service_handler import ServiceHandler
from services.agent_manager import AgentManager
from services.formatter import Formatter

class TestServiceHandler(unittest.TestCase):
    def setUp(self):
        self.agent_manager = AgentManager()
        self.formatter = Formatter()
        self.handler = ServiceHandler(
            io=None, agent_manager=self.agent_manager, formatter=self.formatter
        )
    
    def test_create_agents(self):
        added_roles = ["22-year-old CS student", "CS Professor"]
        self.handler.create_agents(added_roles)
        agent_roles = [agent.role for agent in self.agent_manager.list_of_agents[3:5]]
        result = agent_roles == added_roles
        self.assertEqual(result, True)

    def test_text_in_text_out(self):
        text = "Python is the best language"
        output = self.handler.text_in_text_out(text)
        self.assertIn("You are a farmer", output)
