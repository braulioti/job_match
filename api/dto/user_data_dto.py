"""
User Data DTO
Data for create user
"""

from dataclasses import dataclass


@dataclass
class UserDataDTO:
    """User Response structure"""
    email: str
    password: str
