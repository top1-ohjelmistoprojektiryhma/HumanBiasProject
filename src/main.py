from .services.service_handler import ServiceHandler
from .services.io.console_io import ConsoleIO
from .services.agent_manager import AgentManager


def main():
    io = ConsoleIO()
    agent_manager = AgentManager()
    service_handler = ServiceHandler(io, agent_manager)
    service_handler.start()
