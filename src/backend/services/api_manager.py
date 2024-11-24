import time
from functools import wraps

class RateLimitException(Exception):
    pass

def rate_limiter(max_calls, period):
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            now = time.time()
            # Remove calls that are outside the time window
            calls = [call for call in calls if call > now - period]
            if len(calls) >= max_calls:
                raise RateLimitException("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class ApiManager:
    """Class for managing interaction with multiple APIs"""
    def __init__(
        self,
        gemini_key=None,
        gemini_api=None,
        openai_key=None,
        openai_api=None,
        anthropic_key=None,
        anthropic_api=None):

        self.gemini_key = gemini_key
        self.gemini_api = gemini_api
        self.openai_key = openai_key
        self.openai_api = openai_api
        self.anthropic_key = anthropic_key
        self.anthropic_api = anthropic_api

    @rate_limiter(500, 86400)
    def send_prompts(self, prompt_list):
        """Sends any number of prompts to available or selected models

        Args:
            prompt_list (list): List of dictionaries: 
            [{"text": prompt, "model": model_name, "history": history, "agent_object": agent}]

        Returns:
            list: List of dictionaries containing given prompt, model name, and the model's response
        """
        model_functions = {
            "gemini": self.gemini_api.get_chat_response if self.gemini_key else None,
            "openai": self.openai_api.get_chat_response if self.openai_key else None,
            "anthropic": self.anthropic_api.get_chat_response if self.anthropic_key else None
        }
        # Filter out None values
        model_map = {model: func for model, func in model_functions.items() if func is not None}
        if not model_map:
            return []
        response_list = []
        model_names = list(model_map.keys())

        for i, prompt in enumerate(prompt_list):
            if not prompt["model"]:
                model_name = model_names[i % len(model_names)]
            else:
                model_name = prompt["model"]
            response = model_map[model_name](prompt["text"], prompt["history"])
            response_list.append(
                {
                    "prompt": prompt,
                    "model": model_name,
                    "output": response
                }
            )

        return response_list

    def send_structured_prompt(self, prompt):
        """"
        Sends a prompt to the OpenAI API and returns the response structured as a Class object

        Args:
            prompt (dict): The structured prompt to send to the API:
                {"text": prompt, "model": model_name, "history": history, "agent_object": agent}

        Returns:
            dict: The response from the API structured as a Class object
        """
        if "openai" not in self.available_models():
            return None

        biases = self.openai_api.get_structured_response(prompt)

        return biases

    def available_models(self):
        """Returns a list of available models"""
        available = []
        if self.gemini_key:
            available.append("gemini")
        if self.openai_key:
            available.append("openai")
        if self.anthropic_key:
            available.append("anthropic")
        return available
