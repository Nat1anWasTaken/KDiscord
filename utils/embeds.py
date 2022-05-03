import disnake

from utils.errors import CaseNotFound


class ErrorEmbed(disnake.Embed):
    def __init__(self, message):
        """
        Error Embed Template.
        :param message: The message to include in the embed.
        """
        super().__init__(title="❌錯誤", description=message, color=disnake.Colour.red())
        self.set_footer(text="KDiscord",
                        icon_url="https://cdn.discordapp.com/avatars/811512708721016832/0cb55ba611065513011b899bb7733d38.png?size=1024")


class SuccessEmbed(disnake.Embed):
    def __init__(self, message):
        """
        Success Embed Template.
        :param message: The message to include in the embed.
        """
        super().__init__(title="✅成功", description=message, color=disnake.Colour.green())
        self.set_footer(text="KDiscord",
                        icon_url="https://cdn.discordapp.com/avatars/811512708721016832/0cb55ba611065513011b899bb7733d38.png?size=1024")


class CaseEmbed(disnake.Embed):
    def __init__(self, bot, case_id=None, data=None):
        """
        Case Embed Template
        * Only one of case_id or data should be provided.
        :param bot: The bot instance.
        :param case_id: The case ID.
        :param data: The case data.
        """
        if case_id is None and data is None:
            raise CaseNotFound("Nothing provided")
        elif case_id is not None and data is None:  # Only provided case_id
            case_data = bot.db.cases.find_one({"id": case_id})
            if case_data is None:
                raise CaseNotFound(f"Case ID {case_id} not found")

            # Status and Color
            match case_data["status"]["status"]:
                case "pending":
                    color = disnake.Colour.blue()
                    status = "等待審理"
                case "investigation":
                    color = disnake.Colour.yellow()
                    status = "雙方調查中"
                case "court":
                    color = disnake.Colour.orange()
                    status = "等待開庭"
                case "ended":
                    color = disnake.Colour.green()
                    status = "已結案"
            if case_data["status"]["appeal"]:
                status += "(上訴)"
                color = disnake.Colour.red()
            super().__init__(title="案件資訊", color=color)
            complainant = bot.get_user(case_data["complainant"])
            self.add_field(name="告訴人", value=complainant.mention)
            self.add_field(name="被告人", value=", ".join([f"<@{x}>" for x in case_data["defendants"]]))
            self.add_field(name="狀態", value=status)
            self.add_field(name="案件編號", value=case_data["id"])
            self.set_footer(text="KDiscord",
                            icon_url="https://cdn.discordapp.com/avatars/811512708721016832/0cb55ba611065513011b899bb7733d38.png?size=1024")
            return
        elif case_id is None and data is not None or case_id is not None and data is not None:  # Only provided data or both provided
            match data["status"]["status"]:
                case "pending":
                    color = disnake.Colour.blue()
                    status = "等待審理"
                case "investigation":
                    color = disnake.Colour.yellow()
                    status = "雙方調查中"
                case "court":
                    color = disnake.Colour.orange()
                    status = "等待開庭"
                case "ended":
                    color = disnake.Colour.green()
                    status = "已結案"
            if data["status"]["appeal"]:
                status += "(上訴)"
                color = disnake.Colour.red()
            super().__init__(title="案件資訊", color=color)
            self.add_field(name="告訴人", value=data["complainant"])
            self.add_field(name="被告人", value=", ".join([f"<@{x}>" for x in data["defendants"]]))
            self.add_field(name="狀態", value=status)
            self.add_field(name="案件編號", value=data["id"])
            self.set_footer(text="KDiscord",
                            icon_url="https://cdn.discordapp.com/avatars/811512708721016832/0cb55ba611065513011b899bb7733d38.png?size=1024")
