import re
from pydantic import BaseModel, EmailStr, Field, field_validator, validator
from typing import List, Optional, Type

class Mailbox(BaseModel):
    login: str
    domain: str

    @field_validator('login', 'domain')
    def not_empty(
        cls,
        value: str  # the value to validate
    ) -> str:  # the validated value
        """
        Validate that a given string is not empty.

        Args:
            value: The value to validate.

        Returns:
            The validated value.
        """
        if not value or not value.strip():
            raise ValueError('Value must not be empty')
        return value

    @property
    def email_address(self: 'Mailbox') -> EmailStr:
        """
        Constructs the email address from login and domain.

        Returns:
            EmailStr: The constructed email address.
        """
        return f"{self.login}@{self.domain}"


class Message(BaseModel):
    id: int
    from_email: Optional[str] = Field(None, alias="from")
    subject: Optional[str] = None
    date: Optional[str] = None
    body: Optional[str] = None  
    attachments: Optional[List[str]] = []

    @field_validator('subject', 'date')
    def not_empty(
        cls: Type['Message'],
        value: str  # the value to validate
    ) -> str:  # the validated value
        """
        Validate that a given string is not empty.

        Args:
            value (str): The value to validate.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If the value is empty or contains only whitespace.
        """
        if not value.strip():  # Check if the value is empty or contains only whitespace
            raise ValueError(f'Value {value!r} must not be empty')
        return value
    
    @validator("body", pre=True, always=True)
    def clean_body(cls: Type['Message'], value: Optional[str]) -> Optional[str]:
        """
        Clean the body of the message by removing HTML tags.

        Args:
            value (Optional[str]): The body content of the message.

        Returns:
            Optional[str]: The cleaned message content without HTML tags.
        """
        if value:
            return re.sub('<.*?>', '', value) 
        return value