import openai


class OpenAiApi:
    """Class for managing interaction with OpenAI API"""

    def __init__(self, openai_key=None, model="gpt-4o-mini"):
        self.key = openai_key
        self.model = model
        self.client = openai
        self.client.api_key = self.key

    def get_chat_response(self, prompt, history=None):
        """Sends a prompt to the OpenAI API and returns the response

        Args:
            prompt (str): The prompt to send to the API
            history (list, optional): A list of previous messages of form:
            {"role": user/assistant/system/tool, "content": message}

        Returns:
            str: The response from the API
        """
        chat_history = []
        if history:
            chat_history = self.format_history(history)
        # Add the user's prompt to the chat history
        chat_history.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model, messages=chat_history
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
