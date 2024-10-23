import json


with open("prompts.json", "r", encoding="utf-8") as file:
    PROMPTS = json.load(file)


def format_multiple(role_list, prompt):
    response_list = []
    for role in role_list:
        response_list.append(format_single(role, prompt))
    return response_list


def format_single(role, prompt):
    role = role if role not in (None, "") else "Yourself"
    return PROMPTS["format_single"].format(role=str(role), prompt=str(prompt))


def format_dialog_prompt_with_unseen(agent, unseen_prompts, dialog_format):
    unseen = []
    for prompt in unseen_prompts:
        unseen.append(
            PROMPTS["format_unseen"].format(
                role=prompt["agent"].role, text=prompt["text"]
            )
        )

    formatted_prompt = PROMPTS["format_dialog_prompt_with_unseen"][
        dialog_format
    ].format(role=str(agent.role), unseen=str(unseen))
    return formatted_prompt


def format_generate_agents_prompt(prompt, desired_number_of_agents, list_of_agents):
    """
    Format the prompt to generate the correct number of agents. For formatting reasons,
    desired number of agents must be at least 2. Resulting issues are resolved elsewhere.
    """

    desired_number_of_agents = max(desired_number_of_agents, 2)

    combined_prompt = f"""Generate {str(desired_number_of_agents)} roles to debate the following statement: {str(prompt)}."""  # pylint: disable=line-too-long
    if list_of_agents:
        combined_prompt += f"""Avoid perspectives that overlap with the following roles: {str(list_of_agents)}."""  # pylint: disable=line-too-long

    combined_prompt += "Return a list only in the given style, with the roles separated by '|':\n"  # pylint: disable=line-too-long

    # Handle dynamic agent generation based on the number
    example_for_generation = "|".join(
        [f"agent{i+1}" for i in range(desired_number_of_agents)]
    )
    combined_prompt += example_for_generation

    return combined_prompt
