import re
from . import formatter
from . import agent


class Dialog:
    """Represents a dialog

    Attributes:
        initial_prompt (str): The initial prompt for the dialog
        summarised_prompt (str): The summarised propmpt for the dialog
        agents (list): A dictionary of agents {"AgentObj": {"model": modelname}}
        rounds (dict): A dictionary of rounds identified by round number
        session_format (str): The format of the dialog
        history (list): A list of dictionaries representing the dialog history
    """

    def __init__(
            self,
            initial_prompt="",
            agents=None,
            session_format="dialog",
            summarised_prompt=None
        ):
        self.initial_prompt = initial_prompt
        self.summarised_prompt = summarised_prompt
        self.agents = {} if agents is None else agents
        self.rounds = {}
        self.session_format = session_format
        self.history = []

    def initial_prompts(self, text, agent_list=None, structure="structured"):
        """Get the initial prompts for the dialog

        Args:
            text (str): The initial prompt text"""
        if not agent_list:
            agent_list = list(self.agents.keys())
        input_list = formatter.format_multiple(
            [agent.role for agent in agent_list], text, self.session_format, structure=structure
        )
        prompt_list = []
        # Format the prompts into a list of dictionaries with agent roles and prompts
        for i, prompt in enumerate(input_list):
            model = prompt.get("model", (self.agents[agent_list[i]]["model"], None))
            system_prompt = prompt.get("system_prompt", None) # for openai
            response_format = prompt.get("response_format", None) # for openai
            prompt_list.append({
                "text": prompt["text"],
                "model": model,
                "system_prompt": system_prompt,
                "response_format": response_format,
                "agent": agent_list[i],
                "structure": prompt["structure"]
            })
        return prompt_list

    def get_prompts(self, structure="raw"):
        """Get the prompts for the next round of the dialog"""
        if not self.rounds:
            prompts_list = self.initial_prompts(self.initial_prompt, structure=structure)
        else:
            next_agent = self.get_next_agent()
            unseen_prompts = next_agent.get_unseen_prompts()
            next_agent.reset_unseen_list()
            prompts_list = [formatter.format_dialog_prompt_with_unseen(
                next_agent, unseen_prompts, self.session_format, structure=structure
            )]
            prompts_list[0]["agent"] = next_agent
        api_input_list = []
        for prompt in prompts_list:
            model = prompt.get("model", (self.agents[prompt["agent"]]["model"], None))
            system_prompt = prompt.get("system_prompt", None)
            response_format = prompt.get("response_format", None)
            api_input_list.append(
                {
                    "text": prompt["text"],
                    "model": model,
                    "system_prompt": system_prompt,
                    "response_format": response_format,
                    "history": prompt["agent"].get_chat_history(),
                    "agent_object": prompt["agent"],
                    "structure": prompt["structure"]
                }
            )
        return api_input_list

    def update_with_comment(self, comment):
        """Update the dialog with a comment

        Args:
            comment (str): The comment
        """
        self.add_round(
            len(self.rounds) + 1,
            [
                {
                    "agent": agent.Agent("User"),
                    "model": "User",
                    "input": "None",
                    "output": comment,
                    "summary": "",
                    "conf_score": 50,
                    "score_summary": comment,
                }
            ],
        )
        # Add comment to all agents' unseen list
        for agent_obj in self.agents:
            unseen = [{"agent": agent.Agent("User"), "text": comment}]
            agent_obj.add_unseen_prompts(unseen)

    def extract_response_elements(self, response):
        if isinstance(response["output"], str):
            # if response is unstructured
            # find the summary text from <>
            summary = re.search(r"<.*?>", response["output"])
            summary = summary.group(0)[1:-1].strip() if summary else None
            # Extract the confidence score from |n/10|
            score = re.search(r"\|\s*(\d+)/10\s*\|", response["output"])
            # score between 0-100%
            score = int(score.group(1)) * 10 if score else None
            # Extract score summary from ||summary text||
            score_summary = re.search(r"\|\|.*?\|\|", response["output"])
            score_summary = (
                score_summary.group(0)[2:-2].strip() if score_summary else None
            )
            output = re.sub(r"<\s*.*?\s*>", "", response["output"]).strip()
            output = re.sub(r"\|\d+/10\||\|\|.*?\|\|", "", output).strip()
        else:
            # if response is structured
            structured_output = response["output"]
            output = structured_output.response
            summary = structured_output.main_point_summary
            score = structured_output.score
            score_summary = structured_output.score_summary
        return output, summary, score, score_summary

    def get_summarised_initial_prompt(self, response):
        """Get the summarised initial prompt for the dialog

        Args:
            response (dict): prompt, model and output from the API

        Returns:
            str: The summarised initial prompt for the dialog"""
        api_input = ""
        structure = response["prompt"]["structure"]
        if structure == "structured":
            if response["prompt"]["model"][0] == "openai":
                api_input = self.initial_prompts(
                    self.summarised_prompt,
                    [response["prompt"]["agent_object"]],
                    structure="structured"
                )[0]["system_prompt"]
        else:
            api_input = self.initial_prompts(
                self.summarised_prompt,
                [response["prompt"]["agent_object"]],
                structure="raw"
            )[0]["text"]
        return api_input

    def format_history(self, response, user_input, api_input, structure):
        """Format the chat history

        Args:
            response (dict): The response from the API
            user_input (str): The user input
            api_input (str): The API input
            structure (str): raw/structured

        Returns:
            list: Formatted hitory list.
        """

        history = []
        if structure == "raw":
            history = [
                {"role": "user", "text": api_input},
                {"role": "model", "text": str(response["output"])},
            ]
        elif response["model"][0] == "openai":
            if self.summarised_prompt and len(self.rounds) == 0:
                user_input = self.summarised_prompt
            history = [
                {"role": "system", "text": api_input},
                {"role": "user", "text": user_input},
                {"role": "model", "text": str(response["output"])},
            ]
        return history

    def update_with_responses(self, responses):
        """Update the dialog with responses

        Args:
            responses (list): A list of responses
        """

        prompts = []
        for response in responses:
            output, summary, score, score_summary = self.extract_response_elements(response)
            user_input = response["prompt"].get("text", "")
            structure = response["prompt"]["structure"]
            # Change history input to summarised prompt if needed
            api_input = ""
            if len(self.rounds) == 0 and self.summarised_prompt:
                api_input = self.get_summarised_initial_prompt(response)
            else:
                if structure == "structured":
                    if response["prompt"]["model"][0] == "openai":
                        api_input = response["prompt"]["system_prompt"]
                else:
                    api_input = response["prompt"]["text"]

            # Store the response and add to history
            prompts.append(
                {
                    "agent": response["prompt"]["agent_object"],
                    "model": response["model"],
                    "input": api_input,
                    "output": output,
                    "summary": summary,
                    "conf_score": score,
                    "score_summary": score_summary,
                }
            )
            # Form the history based on the structure and model
            history = self.format_history(response, user_input, api_input, structure)
            response["prompt"]["agent_object"].add_chat_to_history(history)

            # Set model if unset
            if self.agents[response["prompt"]["agent_object"]]["model"] is None:
                self.agents[response["prompt"]["agent_object"]]["model"] = response[
                    "model"][0]

        self.add_round(len(self.rounds) + 1, prompts)
        for agent_obj in self.agents:
            unseen = [prompt for prompt in prompts if prompt["agent"] != agent_obj]
            if unseen:
                self.add_unseen_prompts(agent_obj, unseen)

    def add_unseen_prompts(self, agent_obj, unseen):
        """Add unseen prompts to an agent's unseen list

        Args:
            agent_obj (Agent): The agent object
            unseen (list): A list of unseen prompts
        """
        # Remove |n/10| score and ||summary|| from the unseen prompts
        unseen = [
            {
                "agent": prompt["agent"],
                "text": re.sub(r"\|\d+/10\||\|\|.*?\|\|", "", prompt["output"]).strip(),
            }
            for prompt in unseen
        ]
        agent_obj.add_unseen_prompts(unseen)

    def add_round(self, round_num, prompts):
        """Add a round to the dialog

        Args:
            round_num (int): The round number
            prompts (list): A list of prompts"""
        self.rounds[round_num] = prompts
        self.history.append({"round": round_num, "prompts": prompts})

    def get_next_agent(self):
        """Get the next agent to speak

        Returns:
            Agent: The next agent to speak
        """
        next_agent = None
        agents = list(self.agents.keys())
        if self.session_format in (
            "dialog - no consensus",
            "dialog - consensus",
            "bias finder",
        ):
            next_agent = agents[(len(self.rounds) - 1) % len(agents)]
        else:
            print("DIALOG.PY: Agent is None")
        return next_agent

    def get_agent_history(self, agent_obj):
        """Get the dialog history for a specific agent

        Args:
            agent_obj (Agent): The agent object

        Returns:
            list: A list of dictionaries representing the dialog history
        """
        history = []
        for _, prompts in self.rounds.items():
            for p in prompts:
                if p["agent"] == agent_obj:
                    history.append({"role": "user", "text": p["input"]})
                    history.append({"role": "model", "text": p["output"]})
        return history

    def get_history(self):
        return self.history

    def to_dict(self):
        init = self.initial_prompt
        rounds = {}
        for r, prompts in self.rounds.items():
            rounds[r] = []
            for p in prompts:
                agent_role = p["agent"].role if p["agent"] is not None else "User"
                rounds[r].append(
                    {
                        "agent": agent_role,
                        "model": p["model"],
                        "input": p["input"],
                        "output": p["output"],
                        "summary": p["summary"],
                        "conf_score": p["conf_score"],
                        "score_summary": p["score_summary"],
                    }
                )
        return {"initial_prompt": init, "rounds": rounds}

    def __str__(self):
        def truncate(text, length=30):
            return text[:length] + "..." if len(text) > length else text

        formatted_rounds = ",\n  ".join(
            f"{k}: ["
            + ", \\\n    ".join(
                str(
                    {
                        "agent": p["agent"],
                        "model": p["model"],
                        "input": truncate(p["input"]),
                        "output": truncate(p["output"]),
                    }
                )
                for p in v
            )
            + "]"
            for k, v in self.rounds.items()
        )

        return (
            f"{{\n"
            f"  'initial_prompt': '{self.initial_prompt}',\n"
            f"  'rounds': {{\n  {formatted_rounds}\n  }}\n"
            f"}}"
        )
