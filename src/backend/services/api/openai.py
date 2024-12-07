import openai
from .helpers import get_prompt_fields


class OpenAiApi:
    """Class for managing interaction with OpenAI API"""

    def __init__(self, openai_key=None, default_model="gpt-4o"):
        self.key = openai_key
        self.default_model = default_model
        self.client = openai
        self.client.api_key = self.key

    def get_response(self, prompt):
        """Sends a prompt to the OpenAI API and returns the response

        Args:
            prompt (dict): The structured prompt to send to the API:
            {
            "model": (model, version),
            "system_prompt": str (optional),
            "user_input": str,
            "response_format": class (optional),
            "history": list of previous messages (optional)
            }

        Returns:
            str or class: The response from the API, either as a string or a structured class
        """
        version, history, response_format = self.extract_prompt_elements(prompt)
        print(f"history: {history}")
        if response_format:
            completion = self.client.beta.chat.completions.parse(
                model=version,
                messages=history,
                response_format=response_format,
            )
            print(f"structured response: {completion.choices[0].message.parsed}")
            return completion.choices[0].message.parsed
        else:
            completion = self.client.chat.completions.create(
                model=version,
                messages=history,
            )
            print(f"raw response: {completion.choices[0].message.content}")
            return completion.choices[0].message.content

    def format_history(self, history):
        """Formats the chat history

        Args:
            history (list): list of prompts {"role": user/assistant, "content": message}

        Returns:
            list: A list of dictionaries representing the history
        """
        #pylint: disable=duplicate-code
        formatted_history = []
        for message in history:
            if message["role"] == "user":
                role = "user"
            else:
                role = "assistant"
            formatted_history.append(
                {
                    "role": role, "content": message["text"]
                }
            )
        return formatted_history
        #pylint: enable=duplicate-code

    def extract_prompt_elements(self, prompt):
        """Extracts the prompt elements from the prompt dictionary

        Args:
            prompt (dict): The prompt dictionary

        Returns:
            tuple: Version of the model, history, and response format
        """
        version, system_prompt, user_input, response_format, history = get_prompt_fields(prompt)
        if not version:
            version = self.default_model

        # if history exists, format it and add system prompt and user input
        if history:
            history = self.format_history(history)
        else:
            history = []
        if system_prompt:
            history.append({"role": "system", "content": system_prompt})
        history.append({"role": "user", "content": user_input})

        return version, history, response_format
