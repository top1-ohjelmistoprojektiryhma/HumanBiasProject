import google.generativeai as genai


class ApiManager:
    """Class for managing interaction with multiple APIs"""
    def __init__(self, gemini_key=None, gemini_api=None) -> None:
        self.gemini_key = gemini_key
        self.gemini_api = gemini_api

    def add_gemini_key(self, key):
        "If input key is not None, add new key"
        if key is not None:
            self.gemini_key = key
            genai.configure(api_key=self.gemini_key)
            return True
        return False

    def send_prompts(self, prompt_list):
        """Sends any number of prompts to available or selected models

        Args:
            prompt_list (list): List of dictionaries: 
            [{"text": "prompt text", "model": "model name"}]

        Returns:
            list: List of dictionaries containing given prompt, model name, and the model's response
        """

        model_map = {
            "gemini": self.gemini_api.get_chat_response
        }
        response_list = []
        model_names = list(model_map.keys())

        for i, prompt in enumerate(prompt_list):
            if not prompt["model"]:
                model_name = model_names[i % len(model_names)]
            else:
                model_name = prompt["model"]
            response = model_map[model_name](prompt["text"])
            response_list.append({"prompt": prompt, "model": model_name, "output": response})

        return response_list
