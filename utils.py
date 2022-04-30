import discord
import re
from errors import *


async def find_user_by_name_and_tag(text: str, guild: discord.Guild, multiple: bool = True):
    """
    Find a user by raw text like "NathanTW#9737"
    :param text: Raw text to search for
    :param multiple: If True, text will be splitted by "," and each user will be searched
    :return: A list of members or a single member
    """
    if multiple:
        users = text.split(",")
        # Check if each user is valid
        for user in users:
            if not bool(re.match("^.{2,32}#\d{4}", user)):
                raise UnparseableText(f"{user} is not a valid user")
        # Search for each user
        result = []
        for member in guild.members:
            if f"{member.name}#{member.discriminator}" in users:
                result.append(member)
        return result
    else:
        if not bool(re.match("^.{2,32}#\d{4}", text)):
            raise UnparseableText(f"{text} is not a valid user")
        for member in guild.members:
            if f"{member.name}#{member.discriminator}" == text:
                return member

