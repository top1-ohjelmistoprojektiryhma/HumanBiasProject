import unittest
from unittest.mock import Mock
from backend.services.dialog_manager import DialogManager


class TestDialogManager(unittest.TestCase):
    def setUp(self):
        self._manager = DialogManager()
    
    def test_new_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None, dialog_format="dialog")
        self.assertEqual(dialog_id, 0)
        self.assertEqual(dialog.initial_prompt, "Initial prompt")

    def test_add_round_works(self):
        agent1 = Mock()
        agent2 = Mock()
        agent1.unseen = {}
        agent2.unseen = {}
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None, dialog_format="dialog")
        prompts = [
            {
                "agent": agent1,
                "model": "model1",
                "input": "Prompt 1",
                "output": "Output 1"
            },
            {
                "agent": agent2,
                "model": "model2",
                "input": "Prompt 2",
                "output": "Output 2"
            }
        ]
        self._manager.add_round_to_dialog(dialog_id, 1, prompts)
        self.assertEqual(dialog.rounds, {1: prompts})
        self.assertEqual(agent1.unseen, {0: [{"agent": agent2, "output": "Output 2"}]})
        self.assertEqual(agent2.unseen, {0: [{"agent": agent1, "output": "Output 1"}]})

    def test_get_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None, dialog_format="dialog")
        self.assertEqual(self._manager.get_dialog(dialog_id), dialog)
    
    def test_delete_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None, dialog_format="dialog")
        self._manager.delete_dialog(dialog_id)
        self.assertEqual(self._manager.dialogs, {})

    def test_all_dialogs_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None, dialog_format="dialog")
        self.assertEqual(self._manager.all_dialogs(), {dialog_id: dialog.to_dict()})
