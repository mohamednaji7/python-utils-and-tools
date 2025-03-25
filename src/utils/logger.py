import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

install()
console = Console()

class Logger:
    def __init__(self, rich_print_or_logs='rich_print'):
        self.rich_print_or_log = rich_print_or_logs
        if self.rich_print_or_log == 'rich_print':
            self.logger = console.print
        else:
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[RichHandler(console=console)]
            )
            self.logger = logging.getLogger("rich")

logger = Logger("logs").logger  # Instantiate logger globally
