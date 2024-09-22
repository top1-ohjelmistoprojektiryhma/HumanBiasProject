class Agent:
    """Class representing a singular agent, currently stroring only the role but left to be expanded
    Attributes:
        role (str): The role of the agent

    """

    def __init__(self, role) -> None:
        self.role = str(role)
