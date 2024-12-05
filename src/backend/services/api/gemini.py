import google.generativeai as genai


class GeminiApi:
    """Class for managing interaction with the Gemini API"""

    def __init__(self, gemini_key=None, default_model="gemini-1.5-flash") -> None:
        self.key = gemini_key
        self.default_model = default_model
        genai.configure(api_key=self.key)

    def get_chat_response(self, prompt):
        """Sends a prompt to the Gemini API and returns the response

        Args:
            prompt (str): The prompt to send to the API
            history (list, optional): A list of previous messages of form:
            {"parts": [{"text": message}], "role": user/model}

        Returns:
            str: The response from the API
        """
        history = prompt["history"]
        input = prompt["text"]
        version = prompt["model"][1]

        chat_history = []
        if history:
            chat_history = self.format_history(history)
        text_responses = []
        model = self.init_model(version)
        chat = model.start_chat(history=chat_history)
        responses = chat.send_message(input)
        for chunk in responses:
            text_responses.append(chunk.text)
        return "".join(text_responses)

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
