# backend/app/core/background.py
from fastapi import BackgroundTasks
from typing import Callable, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

async def run_background_task(func: Callable, *args, **kwargs) -> None:
    """
    Run a function as a background task.
    
    Args:
        func: The function to run
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
    """
    try:
        if asyncio.iscoroutinefunction(func):
            await func(*args, **kwargs)
        else:
            func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in background task {func.__name__}: {e}", exc_info=True)

def add_background_task(
    background_tasks: BackgroundTasks,
    func: Callable,
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Add a function to background tasks.
    
    Args:
        background_tasks: FastAPI BackgroundTasks instance
        func: The function to run
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
    """
    background_tasks.add_task(run_background_task, func, *args, **kwargs)
