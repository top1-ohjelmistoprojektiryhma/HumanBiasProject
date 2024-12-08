def get_prompt_fields(prompt):
    """Extracts the prompt elements from the prompt dictionary

    Args:
        prompt (dict): The prompt dictionary

    Returns:
        tuple: The model, system prompt, user input, response format, and history
    """
    # check if model, system_prompt, user_input, response_format, and history are in the prompt
    model = prompt.get("model", None)
    version = None
    if isinstance(model, tuple):
        version = model[1]
    system_prompt = prompt.get("system_prompt", None)
    user_input = prompt.get("text", "")
    response_format = prompt.get("response_format", None)
    anthropic_tools = prompt.get("tools", [])
    history = prompt.get("history", None)

    return version, system_prompt, user_input, response_format, history, anthropic_tools
