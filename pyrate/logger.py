"""
Logging utilities for PyRate Framework.

Provides colorized console output for different log levels using colorama.
"""

from colorama import init, Fore, Style

init(autoreset=True)


def log_step(step_name: str) -> None:
    """
    Log the execution of a test step.
    
    Args:
        step_name: Name/description of the step being executed
    """
    print(f"{Fore.CYAN}ℹ️  Ejecutando: {Style.RESET_ALL}{step_name}")


def log_success(message: str) -> None:
    """
    Log a success message.
    
    Args:
        message: Success message to display
    """
    print(f"{Fore.GREEN}   ✅ {message}")


def log_error(step: str, message: str) -> None:
    """
    Log an error that occurred during test execution.
    
    Args:
        step: The step where the error occurred
        message: Detailed error message
    """
    print(f"\n{Fore.RED}{Style.BRIGHT}🛑 ERROR DE EJECUCIÓN:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   👉 Paso: {step}")
    print(f"{Fore.RED}   🔍 Detalle: {message}\n")


def log_info(message: str) -> None:
    """
    Log an informational message.
    
    Args:
        message: Info message to display
    """
    print(f"{Fore.BLUE}   ℹ️ {message}")


def log_warning(message: str) -> None:
    """
    Log a warning message (non-critical issues).
    
    Args:
        message: Warning message to display
    """
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")


def log_debug(message: str) -> None:
    """
    Log a debug message (for verbose mode).
    
    Args:
        message: Debug message to display
    """
    print(f"{Fore.MAGENTA}🐛 [DEBUG] {message}{Style.RESET_ALL}")