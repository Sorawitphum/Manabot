from discord.ext import commands
import discord

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")  ###ตั้งชื่อห้องที่ต้องการ
        if channel:
            await channel.send(f"🎉 ยินดีต้อนรับ {member.mention} เข้าสู่เซิร์ฟเวอร์!")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
