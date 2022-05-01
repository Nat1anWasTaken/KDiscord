import discord
import re
from errors import *


async def find_user_by_name_and_tag(text: str, guild: discord.Guild, multiple: bool = True):
    """
    Find a user by raw text like "NathanTW#9737"
    :param guild: The guild to search in
    :param text: Raw text to search for
    :param multiple: If True, text will be splitted by "," and each user will be searched
    :return: A list of members or a single member
    """
    if multiple:
        users = text.split(",")
        result = []
        # Find users in the guild,
        # If username and discriminator equals to the target user, add them to the result list
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


async def has_admin(bot_config: dict, member: discord.Member):
    """
    Check if a member has admin roles
    :param bot_config: The bot config
    :param member: The member to check
    :return: True if the member has admin permissions
    """
    for role in member.roles:
        if role.id in bot_config["admin_roles"]:
            return True
    return False
