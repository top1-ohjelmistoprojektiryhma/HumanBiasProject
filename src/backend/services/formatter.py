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

    def format_generate_agents_prompt(self, prompt):
        return f"""{str(prompt)}
        Give 3 perspectives that might be interested adding their thoughts to this statement. 
        Return a list only in this style but replace agents with the actual perspectives: 
        'agent1|agent2|agent3'"""
