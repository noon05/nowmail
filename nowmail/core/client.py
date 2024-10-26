from typing import List

from nowmail.core.models import Message
from nowmail.services.mail_service import Tempmail


class TempMailClient:
    """
    A client for interacting with the tempmail service.

    This class provides a context manager interface, allowing you to use it like this:

        async with TempMailClient() as client:
            # Use the client
    """
    def __init__(self):
        self._mail_service = None

    async def __aenter__(self):
        self._mail_service = Tempmail()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._mail_service.close()

    async def generate_random_mailbox(self, count: int = 1) -> List[str]:
        """
        Generate a specified number of random mailboxes.

        Args:
            count (int): The number of mailboxes to generate.

        Returns:
            List[str]: A list of generated mailbox addresses.
        """
        return await self._mail_service.generate_random_mailbox(count)

    async def check_mailbox(self, login: str, domain: str) -> List[Message]:
        """
        Check a mailbox for new messages.

        Args:
            login (str): The login of the mailbox.
            domain (str): The domain of the mailbox.

        Returns:
            List[Message]: A list of messages in the mailbox.
        """
        return await self._mail_service.check_mailbox(login, domain)

    async def fetch_message(self, login: str, domain: str, message_id: int) -> Message:
        """
        Get a message from a mailbox by ID.

        Args:
            login (str): The login of the mailbox.
            domain (str): The domain of the mailbox.
            message_id (int): The ID of the message to retrieve.

        Returns:
            Message: The message with full details including content.
        """
        return await self._mail_service.fetch_message(login, domain, message_id)