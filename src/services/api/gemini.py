import google.generativeai as genai


class GeminiApi:
    def __init__(self, gemini_key=None, model="gemini-1.5-flash") -> None:
        self.key = gemini_key
        genai.configure(api_key=self.key)
        self.model = genai.GenerativeModel(model)

    def get_chat_response(self, prompt, history=None):
        if not history:
            history = []
        text_responses = []
        chat = self.model.start_chat(history=history)
        responses = chat.send_message(prompt)
        for chunk in responses:
            text_responses.append(chunk.text)
        return "".join(text_responses)
