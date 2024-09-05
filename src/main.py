from services.service_handler import ServiceHandler
from services.io.console_io import ConsoleIO
from services.agent_manager import AgentManager
from services.formatter import Formatter


def main():
    io = ConsoleIO()
    agent_manager = AgentManager()
    formatter = Formatter()
    service_handler = ServiceHandler(io, agent_manager, formatter)
    service_handler.start()


if __name__ == "__main__":
    main()
