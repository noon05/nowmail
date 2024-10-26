import queue
from typing import Callable, List, Optional

from nowmail.core.models import Message
from nowmail.api.async_api import async_check, async_fetch
import asyncio
import time
import threading
from queue import Queue

class PeriodicChecker:
    def __init__(
        self,
        login: str,
        domain: str,
        interval: int,
        duration: int,
    ) -> None:
        """
        Initialize a PeriodicChecker.

        Args:
            login (str): The login of the mailbox.
            domain (str): The domain of the mailbox.
            interval (int): The interval in seconds between checks.
            duration (int): The duration in seconds to check the mailbox.

        Returns:
            None
        """
        self.login = login
        self.domain = domain
        self.interval = interval
        self.duration = duration
        self._stop_event = threading.Event()
        self.result_queue = Queue()

    async def start(self) -> None:
        """
        Start the periodic mailbox check.

        Returns:
            None
        """
        print(f"[INFO] Starting periodic mailbox check for {self.login}@{self.domain} every {self.interval} seconds for {self.duration} seconds.")
        start_time = time.monotonic()

        while not self._stop_event.is_set():
            elapsed_time = time.monotonic() - start_time
            if elapsed_time >= self.duration:
                print(f"[INFO] Stopping periodic mailbox check for {self.login}@{self.domain}. Duration reached.")
                break

            try:
                messages: List[Message] = await async_check(self.login, self.domain)
                if messages:
                    for message in messages:
                        fetched_message: Message = await async_fetch(self.login, self.domain, message.id)
                        self.result_queue.put(fetched_message)
                        self._stop_event.set()
                        return
                else:
                    print(f"[DEBUG] No new messages in mailbox {self.login}@{self.domain}.")
            except Exception as e:
                print(f"[ERROR] An error occurred while checking the mailbox: {e}")
            await asyncio.sleep(self.interval)

    def start_in_thread(self) -> tuple[threading.Thread, queue.Queue[Message]]:
        """
        Start the periodic mailbox check in a separate thread.

        Returns:
            tuple[threading.Thread, queue.Queue[Message]]: The thread object and the queue where the results are stored.
        """

        def run_in_thread():
            """
            Run the periodic mailbox check in a separate event loop.
            """
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.start())
            finally:
                loop.close()

        check_thread = threading.Thread(target=run_in_thread, daemon=True)
        check_thread.start()
        return check_thread, self.result_queue

    def stop(self) -> None:
        """
        Stop the periodic mailbox check.

        This function sets a stop event that the checker thread is waiting on. Once set, the checker thread will exit its loop and finish execution.

        Returns:
            None
        """
        self._stop_event.set()


def start_checker(
    login: str,
    domain: str,
    interval: int,
    duration: int
) -> Callable[[], Optional[Message]]:
    """Start a periodic mailbox checker in a separate thread.

    Args:
        login (str): The login of the mailbox.
        domain (str): The domain of the mailbox.
        interval (int): The interval in seconds between checks.
        duration (int): The duration in seconds to check the mailbox.

    Returns:
        A function that returns the result of the checker when called.
        The result is `None` if the checker has not finished yet.
    """
    checker = PeriodicChecker(login, domain, interval, duration)
    thread, result_queue = checker.start_in_thread()

    def get_result() -> Optional[Message]:
        """Get the result of the periodic mailbox checker.

        The result is `None` if the checker has not finished yet.

        Returns:
            Optional[Message]: The result of the checker, or `None` if it has not finished yet.
        """
        thread.join()  
        if not result_queue.empty():
            return result_queue.get()
        return None

    return get_result