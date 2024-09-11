import google.generativeai as genai


class ApiManager:
    def __init__(self) -> None:
        self.gemini_key = None

    def add_gemini_key(self, key):
        "If input key is not None, add new key"
        if key is not None:
            self.gemini_key = key
            genai.configure(api_key=self.gemini_key)
            return True
        return False

    def send_gemini_prompt(self, prompt):
        response = ""
        if self.gemini_key is not None and prompt != "":
            # try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(str(prompt))
            # except:
            #     response = "key_error"
        return response
