import unittest
from backend.services.dialog import Dialog


class ExampleAgent:
    def __init__(self):
        self.role = "student"

    def get_chat_history(self):
        return ["history"]

    def get_unseen_prompts(self):
        return [{"agent": self, "text": "unseen prompt"}]

class TestDialog(unittest.TestCase):
    def setUp(self):
        self.test_agents = [ExampleAgent(), ExampleAgent()]
        self.dialog = Dialog(
            "Initial prompt",
            {self.test_agents[0]: {"model":"None"}, self.test_agents[1]: {"model":"None"}},
            "dialog - no consensus"
        )

    def test_initial_prompts_works(self):
        """Result should look like:
        list = [{"agent": AgentObject, "text": "prompt"} for agent in ...]
        """
        result = self.dialog.initial_prompts("initial prompt")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["agent"], self.test_agents[0])
        self.assertEqual(result[1]["agent"], self.test_agents[1])
        self.assertTrue(result[0]["text"].startswith("Speak from the following perspective: student"))
        self.assertTrue(result[1]["text"].startswith("Speak from the following perspective: student"))

    def test_get_prompts_works_at_start(self):
        """ Result should look like this:
        list = [{"text": "prompt",
        "model": "modelname", "history": [history], "agent_object": AgentObject}
        for agent ...]
        """
        result = self.dialog.get_prompts()
        self.assertEqual(result[0]["model"], "None")
        self.assertEqual(result[1]["model"], "None")
        self.assertListEqual(result[0]["history"], ["history"])
        self.assertListEqual(result[1]["history"], ["history"])
        self.assertEqual(result[0]["agent_object"], self.test_agents[0])
        self.assertEqual(result[1]["agent_object"], self.test_agents[1])

    def test_get_prompts_works_after_first_round(self):
        self.dialog.rounds["2"] = ["test"]
        result = self.dialog.get_prompts()
        self.assertEqual(result[0]["model"], "None" )
        self.assertListEqual(result[0]["history"], ["history"])
        self.assertEqual(result[0]["agent_object"], self.test_agents[0])

    def test_add_round_works(self):
        self.dialog.add_round(1, ["Prompt 1", "Prompt 2"])
        self.assertEqual(self.dialog.rounds, {1: ["Prompt 1", "Prompt 2"]})

    def test_get_next_agent_works(self):
        self.dialog.add_round(1, ["Prompt 1", "Prompt 2"])
        self.assertEqual(self.dialog.get_next_agent(), self.test_agents[0])
        self.dialog.add_round(2, ["Prompt 3", "Prompt 4"])
        self.assertEqual(self.dialog.get_next_agent(), self.test_agents[1])

    def test_to_dict_works(self):
        self.dialog.add_round(
            1,
            [
                {
                    "agent": ExampleAgent(),
                    "model": "model",
                    "input": "input",
                    "output": "output",
                }
            ],
        )
        self.assertEqual(
            self.dialog.to_dict(),
            {
                "initial_prompt": "Initial prompt",
                "rounds": {
                    1: [
                        {
                            "agent": "student",
                            "model": "model",
                            "input": "input",
                            "output": "output",
                        }
                    ]
                },
            },
        )

    def test_string(self):
        self.dialog.add_round(
            1,
            [
                {
                    "agent": {"role": "agent"},
                    "model": "model",
                    "input": "input",
                    "output": "output",
                }
            ],
        )
        # dont include in coverage
        print(self.dialog)
        self.assertEqual(True, True)

    def test_get_agent_history_works(self):
        agent = ExampleAgent()
        self.dialog.add_round(
            1,
            [{"agent": agent, "model": "model", "input": "input", "output": "output"}],
        )
        self.assertEqual(
            self.dialog.get_agent_history(agent),
            [{"role": "user", "text": "input"}, {"role": "model", "text": "output"}],
        )
