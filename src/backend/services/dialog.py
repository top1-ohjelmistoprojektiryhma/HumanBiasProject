import re
from . import formatter
from . import agent

class Dialog:
    """Represents a dialog

    Attributes:
        initial_prompt (str): The initial prompt for the dialog
        agents (list): A dictionary of agents {"AgentObj": {"model": modelname}}
        rounds (dict): A dictionary of rounds identified by round number
        dialog_format (str): The format of the dialog
        history (list): A list of dictionaries representing the dialog history
    """

    def __init__(self, initial_prompt="", agents=None, dialog_format="dialog"):
        self.initial_prompt = initial_prompt
        self.agents = {} if agents is None else agents
        self.rounds = {}
        self.dialog_format = dialog_format
        self.history = []

    def initial_prompts(self, text):
        """Get the initial prompts for the dialog

        Args:
            text (str): The initial prompt text"""
        agent_list = list(self.agents.keys())
        prompt_list = formatter.format_multiple(
            [agent.role for agent in agent_list], text
        )
        # Format the prompts into a list of dictionaries with agent roles and prompts
        for i, prompt in enumerate(prompt_list):
            prompt_list[i] = {"agent": agent_list[i], "text": prompt}
        return prompt_list

    def get_prompts(self):
        """Get the prompts for the next round of the dialog"""
        if not self.rounds:
            prompts_list = self.initial_prompts(self.initial_prompt)
        else:
            next_agent = self.get_next_agent()
            unseen_prompts = next_agent.get_unseen_prompts()
            prompt = formatter.format_dialog_prompt_with_unseen(
                next_agent, unseen_prompts, self.dialog_format
            )
            prompts_list = [{"agent": next_agent, "text": prompt}]

        api_input_list = [
            {
                "text": prompt["text"],
                "model": self.agents[prompt["agent"]]["model"],
                "history": prompt["agent"].get_chat_history(),
                "agent_object": prompt["agent"],
            }
            for prompt in prompts_list
        ]

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
                }
            ],
        )
        # Add comment to all agents' unseen list
        for agent_obj in self.agents:
            unseen = [{"agent": agent.Agent("User"), "text": comment}]
            agent_obj.add_unseen_prompts(unseen)

    def update_with_responses(self, responses):
        """Update the dialog with responses

        Args:
            responses (list): A list of responses
        """
        prompts = []
        for response in responses:
            # Extract the confidence score using regex
            score_match = re.search(r'\|(\d+)/10\|', response["output"])
            # score between 0-100%
            score = int(score_match.group(1)) * 10 if score_match else None

            # Store the response and add to history
            prompts.append(
                {
                    "agent": response["prompt"]["agent_object"],
                    "model": response["model"],
                    "input": response["prompt"]["text"],
                    "output": response["output"],
                    "conf_score": score,
                }
            )
            response["prompt"]["agent_object"].add_chat_to_history(
                [
                    {"role": "user", "text": response["prompt"]["text"]},
                    {"role": "model", "text": response["output"]},
                ]
            )

            # Set model if unset
            if self.agents[response["prompt"]["agent_object"]]["model"] is None:
                self.agents[response["prompt"]["agent_object"]]["model"] = response[
                    "model"
                ]
   
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
        agent_obj.add_unseen_prompts(
            [{"agent": prompt["agent"], "text": prompt["output"]} for prompt in unseen]
        )

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
        if self.dialog_format in (
            "dialog - no consensus",
            "dialog - consensus",
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
                        "conf_score": p["conf_score"],
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
