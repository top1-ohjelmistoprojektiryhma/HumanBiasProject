class Formatter:
    def __init__(self) -> None:
        pass

    def format_multiple(self, role_list, prompt):
        response_list = []
        for role in role_list:
            response_list.append(self.format_single(role, prompt))
        return response_list

    def format_single(self, role, prompt):
        if role[0].lower() in "aioue":
            role_name = f"an {str(role)}"
        else:
            role_name = f"a {str(role)}"
        return f"""You are {str(role_name)}.
        Give your own thoughts on how probable following statement is: '{str(prompt)}'"""
