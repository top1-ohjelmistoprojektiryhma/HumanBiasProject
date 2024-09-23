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
        Stay grounded and true to character. 
        You are debating the plausibility of the following statement.
        Give a conversational opening statement: {str(prompt)}"""

    def format_single_opening_statement_gemini(self, role, prompt):
        return f"""Embody the following role: {str(role)}.
        Stay grounded and true to character. 
        You are debating the plausibility of the following statement. 
        Give a conversational opening statement: {str(prompt)}"""

    def format_generate_agents_prompt(self, prompt, number_of_agents):
        return f"""{str(prompt)}
        Give {str(number_of_agents)} perspectives that might be interested adding their thoughts to this statement. 
        Return a list only in this style but replace agents with the actual perspectives: 
        agent1|agent2|agent3"""