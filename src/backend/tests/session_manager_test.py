import unittest
from unittest.mock import Mock
from backend.services.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self._manager = SessionManager()
        self.consensus_mock = Mock()
        self.no_consensus_mock = Mock()
        self._manager._all_formats = {"dialog - no consensus":self.no_consensus_mock,
                                      "dialog - consensus":self.consensus_mock}

    def test_new_session_no_consensus_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        expected_call_list = (("Initial prompt", None, "dialog - no consensus"),)
        self.assertEqual(session_id, 0)
        self.assertEqual(expected_call_list, self.no_consensus_mock.call_args)

    def test_new_session_with_incorrect_format_raises_error(self):
        with self.assertRaises(ValueError):
            session_id, session = self._manager.new_session("prompt", agents=None, session_format="no format")

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
        self.assertEqual(self._manager._sessions, {})

    def test_all_sessions_works(self):
        session_id, session = self._manager.new_session(
            "Initial prompt", agents=None, session_format="dialog - no consensus"
        )
        self.assertEqual(self._manager.all_sessions(), {session_id: session.to_dict()})
