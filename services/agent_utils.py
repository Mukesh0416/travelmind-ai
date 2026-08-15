import logging
import time
import os
from functools import wraps
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "travelmind.log"

logger = logging.getLogger("TravelMind")

if not logger.handlers:
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


def log_agent_start(agent_name: str):
    logger.info(f"[Supervisor] Executing {agent_name} Agent")


def log_agent_complete(agent_name: str):
    logger.info(f"[{agent_name} Agent] Completed")


def log_agent_error(agent_name: str, error: Exception):
    logger.error(f"[{agent_name} Agent] Error: {error}")


# ---------------------------------------------------------------------------
# Retry decorator
# ---------------------------------------------------------------------------

def retry(max_retries: int = 3, delay: float = 1.0):
    """
    Retry a function up to `max_retries` times on failure.

    Args:
        max_retries: Maximum number of attempts (default 3).
        delay: Seconds to wait between attempts.

    Returns:
        The decorated function.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_error: Exception = RuntimeError(
                f"{func.__name__} failed after {max_retries} attempts"
            )

            for attempt in range(1, max_retries + 1):

                try:
                    return func(*args, **kwargs)

                except Exception as exc:

                    last_error = exc

                    logger.warning(
                        f"Attempt {attempt}/{max_retries} failed for "
                        f"{func.__name__}: {exc}"
                    )

                    if attempt < max_retries:
                        time.sleep(delay)

            raise last_error

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Safe execution helper
# ---------------------------------------------------------------------------

def safe_execute(
    agent_name: str,
    func,
    *args,
    default=None,
    **kwargs,
):
    """
    Execute a function and return a default value on failure.

    Args:
        agent_name: Name of the agent for logging.
        func: The function to execute.
        default: Value returned on failure.
        *args, **kwargs: Passed to `func`.

    Returns:
        The function result, or `default` on failure.
    """

    try:
        return func(*args, **kwargs)

    except Exception as exc:

        log_agent_error(agent_name, exc)

        return default