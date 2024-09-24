import unittest
from backend.services.dialog_manager import DialogManager


class TestDialogManager(unittest.TestCase):
    def setUp(self):
        self._manager = DialogManager()
    
    def test_new_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None)
        self.assertEqual(dialog_id, 0)
        self.assertEqual(dialog.initial_prompt, "Initial prompt")

    def test_add_round_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None)
        self._manager.add_round_to_dialog(dialog_id, 1, ["Prompt 1", "Prompt 2"])
        self.assertEqual(dialog.rounds, {1: ["Prompt 1", "Prompt 2"]})

    def test_get_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None)
        self.assertEqual(self._manager.get_dialog(dialog_id), dialog)
    
    def test_delete_dialog_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None)
        self._manager.delete_dialog(dialog_id)
        self.assertEqual(self._manager.dialogs, {})

    def test_all_dialogs_works(self):
        dialog_id, dialog = self._manager.new_dialog("Initial prompt", agents=None)
        self.assertEqual(self._manager.all_dialogs(), {dialog_id: dialog.to_dict()})
