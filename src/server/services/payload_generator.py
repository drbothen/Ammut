import random
import string
from typing import Optional

from .base import AbstractPayloadGenerator
from models.enums import PayloadType

class PayloadGenerator(AbstractPayloadGenerator):
    """Generates payloads of a specified size and type."""

    async def generate(self, payload_type: PayloadType, size_kb: int, custom_char: Optional[str] = None) -> str:
        """Generates a payload string."""
        size_bytes = size_kb * 1024
        if payload_type == PayloadType.CUSTOM and custom_char:
            return custom_char * size_bytes
        
        # Default to random payload
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size_bytes))
