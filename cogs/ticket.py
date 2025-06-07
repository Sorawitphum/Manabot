from discord.ext import commands
import discord

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_count = 0

    @commands.command()
    async def ticket(self, ctx, *, reason="ไม่ระบุปัญหา"):
        self.ticket_count += 1
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await ctx.guild.create_text_channel(
            name=f"ticket-{ctx.author.name}-{self.ticket_count}",
            overwrites=overwrites,
            reason="สร้าง Ticket ใหม่"
        )

        await channel.send(f"📩 ขอบคุณ {ctx.author.mention} ที่ติดต่อซัพพอร์ต\nปัญหา: **{reason}**\nทีมงานจะเข้ามาตอบเร็ว ๆ นี้")

async def setup(bot):
    await bot.add_cog(Ticket(bot))
