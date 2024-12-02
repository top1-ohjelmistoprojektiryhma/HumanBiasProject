import anthropic


class AnthropicApi:
    def __init__(self, anthropic_key=None, default_model="claude-3-5-sonnet-latest"):
        self.key = anthropic_key
        self.default_model = default_model
        self.client = anthropic.Anthropic(api_key=self.key)

    def get_chat_response(self, prompt, history=None, version=None):
        """Sends a prompt to the OpenAI API and returns the response

        Args:
            prompt (str): The prompt to send to the API
            history (list, optional): A list of previous messages of form:
            {"role": user/assistant, "content": [{"text": message, "type": "text"}]}

        Returns:
            str: The response from the API
        """
        chat_history = []
        if history:
            chat_history = self.format_history(history)
        # Add the user's prompt to the chat history
        chat_history.append({"role": "user", "content": [{"text": prompt, "type": "text"}]})
        if version:
            model = version
        else:
            model = self.default_model
        message = self.client.messages.create(
            model=model,
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
        return response

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
