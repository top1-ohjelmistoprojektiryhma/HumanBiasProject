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

    def format_generate_agents_prompt(self, prompt, desired_number_of_agents, list_of_agents):


        combined_prompt = f"""Generate {str(desired_number_of_agents)}
        perspectives to debate the following statement: {str(prompt)}
        Avoid perspectives that overlap with the following perspectives: {str(list_of_agents)}
        Return a list only in the given style by replacing each instance of "agent" with the actual perspective: 
        """
        if desired_number_of_agents < 3:
            example_for_generation = "agent1|agent2"
        elif desired_number_of_agents == 3:
            example_for_generation = "agent1|agent2|agent3"
        else:
            example_for_generation =f"agent1|agent2|agent3|...|agent{str(desired_number_of_agents)}"
        combined_prompt = combined_prompt+ example_for_generation

        print(combined_prompt)

        return combined_prompt
