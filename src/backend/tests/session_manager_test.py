import unittest
from unittest.mock import Mock
from backend.services.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self._manager = SessionManager()

    def test_new_session_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        self.assertEqual(session_id, 0)
        self.assertEqual(session.initial_prompt, "Initial prompt")

    def test_get_session_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        self.assertEqual(self._manager.get_session(session_id), session)

    def test_delete_session_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        self._manager.delete_session(session_id)
        self.assertEqual(self._manager.sessions, {})

    def test_all_sessions_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        self.assertEqual(self._manager.all_sessions(), {session_id: session.to_dict()})
