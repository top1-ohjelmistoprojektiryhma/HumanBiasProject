import unittest
from backend.services.dialog import Dialog


class ExampleAgent:
    def __init__(self):
        self.role = "student"
        self.unseen = []
        self.history = []

    def get_chat_history(self):
        return ["history"]

    def get_unseen_prompts(self):
        return [{"agent": self, "text": "unseen prompt"}]

    def add_unseen_prompts(self, prompts):
        self.unseen.extend(prompts)

    def add_chat_to_history(self, chat):
        self.history.extend(chat)


class TestDialog(unittest.TestCase):
    def setUp(self):
        self.test_agents = [ExampleAgent(), ExampleAgent()]
        self.dialog = Dialog(
            "Initial prompt",
            {self.test_agents[0]: {"model": None}, self.test_agents[1]: {"model": "Gemini"}},
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
        self.assertIsNone(result[0]["model"])
        self.assertEqual(result[1]["model"], "Gemini")
        self.assertListEqual(result[0]["history"], ["history"])
        self.assertListEqual(result[1]["history"], ["history"])
        self.assertEqual(result[0]["agent_object"], self.test_agents[0])
        self.assertEqual(result[1]["agent_object"], self.test_agents[1])

    def test_get_prompts_works_after_first_round(self):
        self.dialog.rounds["2"] = ["test"]
        result = self.dialog.get_prompts()
        self.assertIsNone(result[0]["model"])
        self.assertListEqual(result[0]["history"], ["history"])
        self.assertEqual(result[0]["agent_object"], self.test_agents[0])

    def test_update_with_comment_works(self):
        self.dialog.update_with_comment("This is a comment")
        added_round = self.dialog.rounds[1]
        self.assertEqual(added_round[0]["agent"].role, "User")
        self.assertEqual(added_round[0]["model"], "User")
        self.assertEqual(added_round[0]["input"], "None")
        self.assertEqual(added_round[0]["output"], "This is a comment")

        for agent in self.dialog.agents:
            self.assertEqual(agent.unseen[0]["agent"].role, "User")
            self.assertEqual(agent.unseen[0]["text"], "This is a comment")

    def test_update_with_responses_works(self):
        test_responses = [
            {
                "prompt": {
                "agent_object": self.test_agents[0],
                "text": "This is the prompt text"
                },
                "model": "Open_AI",
                "output": "This is the model output"
            },
            {
                "prompt": {
                "agent_object": self.test_agents[1],
                "text": "This is the prompt text"
                },
                "model": "Gemini",
                "output": "This is the model output"
            }
        ]
        self.dialog.update_with_responses(test_responses)
        for agent in self.test_agents:
            self.assertListEqual(agent.history, [
                {"role": "user", "text": "This is the prompt text"},
                {"role": "model", "text": "This is the model output"}
            ])
            self.assertTrue(len(agent.unseen) == 1)

        self.assertEqual(self.dialog.agents[self.test_agents[0]]["model"], "Open_AI")
        self.assertIsNotNone(self.dialog.rounds.get(1, None))

    def test_add_unseen_prompts_works(self):
        test_unseen = [{"agent": "Agent1", "output": "This is the output"}]
        self.dialog.add_unseen_prompts(self.test_agents[0], test_unseen)
        result = self.test_agents[0].unseen
        self.assertListEqual(result, [{"agent": "Agent1", "text": "This is the output"}])

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

    def test_get_history_works(self):
        self.dialog.history.append(":)")
        self.assertListEqual(self.dialog.get_history(), [":)"])
