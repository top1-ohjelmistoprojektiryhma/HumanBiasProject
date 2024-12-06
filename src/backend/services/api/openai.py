import openai
from .helpers import get_prompt_fields


class OpenAiApi:
    """Class for managing interaction with OpenAI API"""

    def __init__(self, openai_key=None, default_model="gpt-4o"):
        self.key = openai_key
        self.default_model = default_model
        self.client = openai
        self.client.api_key = self.key

    def get_chat_response(self, prompt):
        """Sends a prompt to the OpenAI API and returns the response

        Args:
            prompt (dict): parameters related to prompt:
            {"text": prompt, "model": (model, version), "history": history, "agent_object": agent}
        Returns:
            str: The response from the API
        """
        version, history, _ = self.extract_prompt_elements(prompt)
        completion = self.client.chat.completions.create(
            model=version, messages=history
        )
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

    def get_structured_response(self, prompt):
        """Sends a structured prompt to the OpenAI API and returns the response

        Args:
            prompt (dict): The structured prompt to send to the API:
            {
            "model": "gpt-4o-2024-08-06",
            "system_prompt": str,
            "user_input": str,
            "response_format": class
            "history": None (for initial implementation)
            }
    }
        Returns:
            class: KnownBiases{Baias: {bias_name: str, bias_severity: int, reasoning: str}}
        """
        version, history, response_format = self.extract_prompt_elements(prompt)

        client = self.client.OpenAI()

        completion = client.beta.chat.completions.parse(
        model=version,
        messages=history,
        response_format=response_format,
        )

        biases = completion.choices[0].message.parsed

        return biases

    def extract_prompt_elements(self, prompt):
        """Extracts the prompt elements from the prompt dictionary

        Args:
            prompt (dict): The prompt dictionary

        Returns:
            tuple: The model, system prompt, user input, response format, and history
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
