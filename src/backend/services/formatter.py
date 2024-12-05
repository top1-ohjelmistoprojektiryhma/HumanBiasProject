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

def format_output_summary(dialog_data, session_format):
    return PROMPTS["format_output_summary"][session_format].format(
        dialog_data=str(dialog_data)
    )


def format_bias(dialog_data):
    return PROMPTS["format_get_bias"].format(dialog_data=str(dialog_data))


def format_input_summary(words, text):
    return PROMPTS["format_input_summary"].format(words=words, text=text)

def new_roles_to_list_of_roles(new_roles, desired_lenght):

    output_list = []

    if (isinstance(new_roles, object)
        and hasattr(new_roles, 'roles')
        and isinstance(new_roles.roles, list)):

        for role in new_roles.roles:
            name = agent_class_to_str(role)
            if name:
                output_list.append(name)

        if len(output_list) >= desired_lenght:
            return output_list[:desired_lenght]

    return output_list

def agent_class_to_str(role):

    name = None
    if hasattr(role, 'role_description'):
        name = str(role.role_description)
        if name == '':
            name = None
    return name

def format_generate_agents_class_prompt(user_input, current_agents=[],
                                        desired_number_of_agents=3,
                                        session_format="bias finder"):

    class Role(BaseModel):
        role_description: str

    class NewRoles(BaseModel):
        roles: list[Role]

    system_prompt = PROMPTS["format_generate_agents"][session_format].format(
        desired_number_of_agents = str(desired_number_of_agents),
        current_agents = str(current_agents))

    prompt = format_structured_prompt(system_prompt, user_input, NewRoles)

    return prompt

def format_opening_statement_class_prompt(user_input, role, session_format):

    return format_statement_class_prompt(user_input, role, session_format, "format_single_structured_opening_statement", None)

def format_statement_class_prompt(user_input, role, session_format, statement_type = "format_single_structured_opening_statement", history = None):

    class Statement(BaseModel):
        response: str
        score: int
        reasoning: str

    system_prompt = PROMPTS[statement_type][session_format].format(role = str(role))

    prompt = format_structured_prompt(system_prompt, user_input, Statement, history)

    return prompt

def format_bias_class_prompt(user_input):

    class Bias(BaseModel):
        bias_name: str
        bias_severity: int
        reasoning: str

    class KnownBiases(BaseModel):
        biases: list[Bias]

    system_prompt = PROMPTS["format_bias_class"]

    prompt = format_structured_prompt(system_prompt, user_input, KnownBiases)

    return prompt

def format_structured_prompt(system_prompt,
                             user_input,
                             response_format,
                             model="gpt-4o-2024-08-06",
                             history=None):
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
        "model": model,
        "system_prompt": system_prompt,
        "user_input": user_input,
        "response_format": response_format,
        "history": history,
    }

    return prompt

def class_to_json(python_class):
    return json.dumps(python_class, default=lambda o: o.__dict__)
