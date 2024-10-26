import asyncio
import logging
from typing import Any, Dict, List

import aiohttp
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed, retry_if_exception_type

from nowmail.services.exceptions import NetworkError, APIError
from nowmail.services.interfaces import IMailAPIClient
from nowmail.services.config import MailServiceConfig
from nowmail.core.models import Message, Mailbox

logger = logging.getLogger(__name__)


class Tempmail(IMailAPIClient):
    """
    An asynchronous mail service client that uses the 1secmail.com API.

    Attributes:
        config (MailServiceConfig): Configuration for the mail service.
        base_url (str): The base URL of the API.
        timeout (int): The timeout for requests.
        session (aiohttp.ClientSession): The aiohttp session used for requests.
    """
    def __init__(self, config: MailServiceConfig = None) -> None:
        """
        Initialize the AsyncMailService with configuration.

        Args:
            config (MailServiceConfig, optional): Configuration for the mail service. Defaults to None.

        Returns:
            None
        """
        self.config = config or MailServiceConfig()
        self.base_url = self.config.base_url
        self.timeout = self.config.timeout
        self.session = aiohttp.ClientSession()


    async def _make_request(self, params: Dict[str, Any]) -> Any:
        """
        Make a GET request to the MailService API.

        Args:
            params (Dict[str, Any]): The parameters to pass to the API.

        Returns:
            Any: The JSON response from the API.

        Raises:
            NetworkError: If there was a network error.
            APIError: If there was an API error.
        """
        retryer = AsyncRetrying(
            stop=stop_after_attempt(3),
            wait=wait_fixed(2),
            retry=retry_if_exception_type(NetworkError)
        )
        async for attempt in retryer:
            with attempt:
                try:
                    logger.debug(f"Sending asynchronous request with parameters: {params}")
                    async with self.session.get(self.base_url, params=params, timeout=self.timeout) as response:
                        response.raise_for_status()
                        response_json = await response.json()
                        if isinstance(response_json, dict) and 'error' in response_json:
                            raise APIError(f"API error: {response_json['error']}")
                        return response_json
                except aiohttp.ClientError as e:
                    logger.error(f"Network error: {e}")
                    raise NetworkError(f"Network error: {e}")
                except asyncio.TimeoutError as e:
                    logger.error(f"Request timeout: {e}")
                    raise NetworkError(f"Request timeout: {e}")
                except ValueError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    raise APIError(f"Failed to parse JSON response: {e}")


    async def generate_random_mailbox(self, count: int = 1) -> List[str]:
        """
        Generate a specified number of random mailboxes.

        Args:
            count (int): The number of mailboxes to generate.

        Returns:
            List[str]: A list of generated mailbox addresses.
        """
        if count < 1:
            raise ValueError("Parameter count must be greater than 0.")

        mailboxes = []
        for i in range(count):
            params = {'action': 'genRandomMailbox'}
            response_json = await self._make_request(params)

            if isinstance(response_json, str):
                mailboxes.append(response_json)
            elif isinstance(response_json, list):
                mailboxes.extend(response_json)
            else:
                raise APIError("Unexpected response format for mailbox generation.")

        return mailboxes


    async def check_mailbox(self, login: str, domain: str) -> List[Message]:
        """Check a mailbox for new messages.

        Args:
            login (str): The login of the mailbox.
            domain (str): The domain of the mailbox.

        Returns:
            List[Message]: A list of messages in the mailbox.

        Raises:
            APIError: If the API returned an error or an invalid response.
            NetworkError: If there was a network error.
        """
        mailbox = Mailbox(login=login, domain=domain)
        params = {'action': 'getMessages', 'login': mailbox.login, 'domain': mailbox.domain}
        response_json = await self._make_request(params)

        if not isinstance(response_json, list):
            raise APIError(f"Expected a list of messages, received: {type(response_json)}")

        messages = [Message(**msg) for msg in response_json]

        logger.info(f"Found {len(messages)} messages in the mailbox {mailbox.email_address}.")
        return messages


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
        mailbox = Mailbox(login=login, domain=domain)
        params = {
            'action': 'readMessage',  
            'login': mailbox.login,
            'domain': mailbox.domain,
            'id': message_id
        }
        response_json = await self._make_request(params)
        if not isinstance(response_json, dict):
            raise APIError(f"Expected a dictionary with message data, received: {type(response_json)}")

        message = Message(**response_json)
        return message


    async def delete_message(
        self, login: str, domain: str, message_id: int
    ) -> bool:
        """Delete a message from a mailbox by ID.

        Args:
            login (str): The login of the mailbox.
            domain (str): The domain of the mailbox.
            message_id (int): The ID of the message to delete.

        Returns:
            bool: True if the message was successfully deleted.

        Raises:
            APIError: If the API returned an error or an invalid response.
            NetworkError: If there was a network error.
        """
        mailbox = Mailbox(login=login, domain=domain)
        params = {
            'action': 'deleteMessage',
            'login': mailbox.login,
            'domain': mailbox.domain,
            'id': message_id
        }
        response_json = await self._make_request(params)

        if response_json != {}:
            raise APIError(f"Expected an empty response, received: {response_json}")

        logger.info(f"Message with ID {message_id} deleted from mailbox {mailbox.email_address}.")
        return True


    async def close(self) -> None:
        """Close the aiohttp session.

        Returns:
            None
        """
        await self.session.close()