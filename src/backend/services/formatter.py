class Formatter:

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
        """
        Format the prompt to generate the correct number of agents. For formatting reasons,
        desired number of agents must be at least 2. Resulting issues are resolved elsewhere.
        """

        desired_number_of_agents = max(desired_number_of_agents, 2)

        combined_prompt = f"""Generate {str(desired_number_of_agents)} roles to debate the following statement: {str(prompt)}.""" #pylint: disable=line-too-long
        if list_of_agents:
            combined_prompt += f"""Avoid perspectives that overlap with the following roles: {str(list_of_agents)}.""" #pylint: disable=line-too-long

        combined_prompt += "Return a list only in the given style, with the roles separated by '|':\n" #pylint: disable=line-too-long

        # Handle dynamic agent generation based on the number
        example_for_generation = '|'.join([f"agent{i+1}" for i in range(desired_number_of_agents)])
        combined_prompt += example_for_generation

        return combined_prompt
