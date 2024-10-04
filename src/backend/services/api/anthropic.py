import anthropic


class AnthropicApi:
    def __init__(self, anthropic_key=None, model="claude-3-haiku-20240307"):
        self.key = anthropic_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.key)

    def get_chat_response(self, prompt, history=None):
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
        message = self.client.messages.create(
            model=self.model, messages=chat_history, max_tokens=1000
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
