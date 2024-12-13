import anthropic
from .helpers import get_prompt_fields


class AnthropicApi:
    """Class for managing interaction with the Anthropic API
    """
    def __init__(self, anthropic_key=None, default_model="claude-3-5-sonnet-latest"):
        self.key = anthropic_key
        self.default_model = default_model
        self.client = anthropic.Anthropic(api_key=self.key)

    def get_chat_response(self, prompt):
        """Sends a prompt to the OpenAI API and returns the response

        Args:
            prompt (dict): parameters related to prompt:
            {"text": prompt, "model": (model, version), "history": history, "agent_object": agent}

        Returns:
            tuple: The response from the API and the model version
        """
        version, chat_history = self.extract_prompt_elements(prompt)
        message = self.client.messages.create(
            model=version,
            messages=chat_history,
            max_tokens=1000,
            system = """
            Respond only with plain text dialogue. 
            Avoid all stage directions, actions, 
            roleplaying elements, or any text within asterisks or parentheses.
            At all costs avoid repeating yourself""",
            temperature=1.0
        )
        response = "".join([content.text for content in message.content])
        return response, version

    def format_history(self, history):
        """Formats the chat history

        Args:
            history (list): list of prompts 
            {"role": user/assistant, "content": [{"text": message, "type": "text"}]}

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
                    "role": role, "content": [{"text": message["text"], "type": "text"}]
                }
            )
        return formatted_history
        #pylint: enable=duplicate-code

    def extract_prompt_elements(self, prompt):
        """Extracts the prompt elements from the prompt dictionary

        Args:
            prompt (dict): The prompt dictionary

        Returns:
            tuple: The model and history
        """
        version, _system_prompt, user_input, _response_format, history = get_prompt_fields(prompt)
        if not version:
            version = self.default_model

        # if history exists, format it and add system prompt and user input
        if history:
            history = self.format_history(history)
        else:
            history = []
        history.append({"role": "user", "content": [{"text": user_input, "type": "text"}]})

        return version, history
