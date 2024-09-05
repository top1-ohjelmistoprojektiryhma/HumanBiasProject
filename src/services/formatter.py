class Formatter:
    def __init__(self) -> None:
        pass

    def format_multiple(self, role_list, prompt):
        response_list = []
        for role in role_list:
            response_list.append(self.format_single(role, prompt))
        return response_list

    def format_single(self, role, prompt):
        return f"Take on the following role '{str(role)}'. Give a brief anwser on the plausability of the following statement: '{str(prompt)}'"
