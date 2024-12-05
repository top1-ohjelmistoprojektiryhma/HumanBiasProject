import openai


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
            prompt (str): The prompt to send to the API
            history (list, optional): A list of previous messages of form:
            {"role": user/assistant/system/tool, "content": message}

        Returns:
            str: The response from the API
        """
        history = prompt["history"]
        api_input = prompt["text"]
        version = prompt["model"][1]

        chat_history = []
        if history:
            chat_history = self.format_history(history)
        # Add the user's input to the chat history
        chat_history.append({"role": "user", "content": api_input})
        if version:
            model = version
        else:
            model = self.default_model
        completion = self.client.chat.completions.create(
            model=model, messages=chat_history
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

        client = self.client.OpenAI()

        completion = client.beta.chat.completions.parse(
        model=prompt["model"],
        messages=[
            {"role": "system", "content": prompt["system_prompt"]},
            {"role": "user", "content": prompt["user_input"]}
        ],
        response_format=prompt["response_format"],
        )

        biases = completion.choices[0].message.parsed

        return biases
