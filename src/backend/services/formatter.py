import json
from pydantic import BaseModel

with open("prompts.json", "r", encoding="utf-8") as file:
    PROMPTS = json.load(file)


def format_multiple(role_list, prompt, session_format):
    response_list = []
    for role in role_list:
        response_list.append(format_single(role, prompt, session_format))
    return response_list


def format_single(role, prompt, session_format):
    role = role if role not in (None, "") else "Yourself"
    formatted_prompt = PROMPTS["format_single_opening_statement"][
        session_format
    ].format(role=str(role), prompt=str(prompt))

    return formatted_prompt


def format_dialog_prompt_with_unseen(agent, unseen_prompts, session_format):
    unseen = []
    for prompt in unseen_prompts:
        unseen.append(
            PROMPTS["format_unseen"].format(
                role=prompt["agent"].role, text=prompt["text"]
            )
        )

    formatted_prompt = PROMPTS["format_dialog_prompt_with_unseen"][
        session_format
    ].format(role=str(agent.role), unseen=str(unseen))
    return formatted_prompt


def format_generate_agents_prompt(prompt, desired_number_of_agents, list_of_agents):
    """
    Format the prompt to generate the correct number of agents. For formatting reasons,
    desired number of agents must be at least 2. Resulting issues are resolved elsewhere.
    """

    desired_number_of_agents = max(desired_number_of_agents, 2)

    combined_prompt = f"Generate {str(desired_number_of_agents)} roles of a maximum of 5 words to debate the following statement: {str(prompt)}."  # pylint: disable=line-too-long
    if list_of_agents:
        combined_prompt += f"Avoid perspectives that overlap with the following roles: {str(list_of_agents)}."  # pylint: disable=line-too-long

    combined_prompt += "Your response should contain nothing but a list in the given style, with the roles separated by '|':\n"  # pylint: disable=line-too-long
    # Handle dynamic agent generation based on the number
    example_for_generation = "|".join(
        [f"agent{i+1}" for i in range(desired_number_of_agents)]
    )
    combined_prompt += example_for_generation

    return combined_prompt


def format_output_summary(dialog_data, session_format):
    return PROMPTS["format_output_summary"][session_format].format(
        dialog_data=str(dialog_data)
    )


def format_bias(dialog_data):
    return PROMPTS["format_get_bias"].format(dialog_data=str(dialog_data))


def format_input_summary(words, text):
    return PROMPTS["format_input_summary"].format(words=words, text=text)


def class_to_json(python_class):
    return json.dumps(python_class, default=lambda o: o.__dict__)


def format_bias_class(user_input):

    class Bias(BaseModel):
        bias_name: str
        bias_severity: int
        reasoning: str

    class KnownBiases(BaseModel):
        biases: list[Bias]

    system_prompt = PROMPTS["format_bias_class"]

    prompt = format_structured_prompt(system_prompt, user_input, KnownBiases)

    return prompt


def format_structured_prompt(system_prompt, user_input, response_format, history=None):
    """
    Formats a prompt for the OpenAI API with structured response

    Args:
        user_input (str): The user's input
        response_format (class): The response format

    Returns:
        dict: The formatted prompt:
        {
            "model": "gpt-4o-2024-08-06",
            "system_prompt": str,
            "user_input": str,
            "response_format": class
            "history": None (for initial implementation)
        }
    """

    prompt = {
        "model": "gpt-4o-2024-08-06",
        "system_prompt": system_prompt,
        "user_input": user_input,
        "response_format": response_format,
        "history": history,
    }

    return prompt
