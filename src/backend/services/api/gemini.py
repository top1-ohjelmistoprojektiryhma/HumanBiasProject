import google.generativeai as genai
from .helpers import get_prompt_fields


class GeminiApi:
    """Class for managing interaction with the Gemini API"""

    def __init__(self, gemini_key=None, default_model="gemini-1.5-flash") -> None:
        self.key = gemini_key
        self.default_model = default_model
        genai.configure(api_key=self.key)

    def get_chat_response(self, prompt):
        """Sends a prompt to the Gemini API and returns the response

        Args:
            prompt (dict): parameters related to prompt:
            {"text": prompt, "model": (model, version), "history": history, "agent_object": agent}

        Returns:
            str: The response from the API
        """
        version, history, api_input = self.extract_prompt_elements(prompt)
        text_responses = []
        model = self.init_model(version)
        chat = model.start_chat(history=history)
        responses = chat.send_message(api_input)
        for chunk in responses:
            text_responses.append(chunk.text)
        return "".join(text_responses), version

    def format_history(self, history):
        """Formats the chat history

        Args:
            history (list): list of prompts {"role": user/model, "text": message}

        Returns:
            list: A list of dictionaries representing the history
        """
        formatted_history = []
        for message in history:
            formatted_history.append(
                {
                    "parts": [{"text": message["text"]}], "role": message["role"]
                }
            )
        return formatted_history

    def init_model(self, version=None):
        if version:
            return genai.GenerativeModel(version)
        return genai.GenerativeModel(self.default_model)

    def extract_prompt_elements(self, prompt):
        """Extracts the prompt elements from the prompt dictionary

        Args:
            prompt (dict): The prompt dictionary

        Returns:
            tuple: The model, history, and user input"""
        version, system_prompt, user_input, response_format, history = get_prompt_fields(prompt)
        if not version:
            version = self.default_model

        # if history exists, format it and add system prompt and user input
        if history:
            history = self.format_history(history)
        else:
            history = []

        return version, history, user_input
