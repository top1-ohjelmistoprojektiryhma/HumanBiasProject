class Formatter:
    def __init__(self) -> None:
        pass

    def format_multiple(self, role_list, prompt):
        response_list = []
        for role in role_list:
            response_list.append(self.format_single(role, prompt))
        return response_list

    def format_single(self, role, prompt):
        role = role if role not in (None, "") else "Yourself"
        return f"""Embody the following role: {str(role)}.
        Give briefly your own thoughts on how probable the following statement is: {str(prompt)}"""
