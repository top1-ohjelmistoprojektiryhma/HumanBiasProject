from .services.service_handler import ServiceHandler
from .services.io.console_io import ConsoleIO

def main():
    io = ConsoleIO()
    service_handler = ServiceHandler(io)
    service_handler.start()