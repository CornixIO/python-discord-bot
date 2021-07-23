from discord_bot.common.endpoints import BASE_URL, GET_GUILD, GET_GUILD_PREVIEW, GUILD_ICON, GET_GUILD_ROLES, \
    GET_GUILD_MEMBERS
from discord_bot.common.request import Request
from discord_bot.models.guild import Guild
from discord_bot.models.member import Member
from discord_bot.models.role import Role
from discord_bot.models.user import User


class GuildAPI(object):
    def __init__(self, token):
        self.token = token

    def get_guild(self, guild_id):
        url = BASE_URL + GET_GUILD.format(guild_id)
        request = Request(self.token, url, "GET")
        payload = request.execute()
        return Guild(**payload)

    def get_guild_preview(self, guild_id):
        url = BASE_URL + GET_GUILD_PREVIEW.format(guild_id)
        request = Request(self.token, url, "GET")
        payload = request.execute()
        return Guild(**payload)

    @staticmethod
    def get_guild_icon_url(guild_id, icon_hash):
        return GUILD_ICON.format(guild_id, icon_hash)

    @staticmethod
    def _parse_role(role_payload):
        return Role(**role_payload)

    def get_guild_roles(self, guild_id):
        url = BASE_URL + GET_GUILD_ROLES.format(guild_id)
        request = Request(self.token, url, "GET")
        payload = request.execute()
        roles = list()
        for role_payload in payload:
            roles.append(self._parse_role(role_payload))
        return roles

    @staticmethod
    def _parse_member(member_payload):
        member_payload["user"] = User(**member_payload["user"])
        return Member(**member_payload)

    def _get_guild_members_batch(self, base_url, last_user_id=None, limit=1000):
        url = base_url
        if last_user_id:
            url += "?" + f"after={last_user_id}"
        if limit:
            url += "?" + f"limit={limit}"
        request = Request(self.token, url, "GET")
        payload = request.execute()
        members = list()
        for member_payload in payload:
            members.append(self._parse_member(member_payload))
        return members

    def get_guild_members(self, guild_id, force_all=False):
        url = BASE_URL + GET_GUILD_MEMBERS.format(guild_id)
        limit = 1000
        users = current_batch = self._get_guild_members_batch(url, limit=limit)
        while force_all and len(current_batch) >= limit:
            last_user = current_batch[-1]
            last_user_id = last_user.user.id
            current_batch = self._get_guild_members_batch(url, last_user_id=last_user_id, limit=limit)
            users.extend(current_batch)

        return users
