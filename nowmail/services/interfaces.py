# interfaces.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from nowmail.core.models import Message


class IMailAPIClient(ABC):
    @abstractmethod
    def generate_random_mailbox(self, count: int) -> List[str]:
        """Generate a list of random mailboxes."""

    @abstractmethod
    def check_mailbox(self, login: str, domain: str) -> List[Message]:
        """Check a mailbox for new messages."""

    @abstractmethod
    def fetch_message(self, login: str, domain: str, message_id: int) -> Message:
        """Get a message from a mailbox by ID."""

    @abstractmethod
    def delete_message(self, login: str, domain: str, message_id: int) -> bool:
        """Delete a message from a mailbox by ID. Not support now"""