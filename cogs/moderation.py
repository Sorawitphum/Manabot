import discord
from discord.ext import commands
import datetime
import config

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", description="เตะผู้ใช้ออกจากเซิร์ฟเวอร์")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "ไม่มีเหตุผล"):
        """คำสั่งเตะผู้ใช้ออกจากเซิร์ฟเวอร์"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send(config.ERROR_MESSAGES["role_hierarchy"])
            return

        try:
            await member.kick(reason=f"เตะโดย {ctx.author.name}: {reason}")
            embed = discord.Embed(
                title=config.SUCCESS_MESSAGES["kick"],
                description=f"**ผู้ใช้:** {member.mention}\n**เหตุผล:** {reason}",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"ดำเนินการโดย {ctx.author.name}")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(config.ERROR_MESSAGES["bot_permission"])
        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    @commands.command(name="ban", description="แบนผู้ใช้จากเซิร์ฟเวอร์")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "ไม่มีเหตุผล"):
        """คำสั่งแบนผู้ใช้จากเซิร์ฟเวอร์"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send(config.ERROR_MESSAGES["role_hierarchy"])
            return

        try:
            await member.ban(reason=f"แบนโดย {ctx.author.name}: {reason}")
            embed = discord.Embed(
                title=config.SUCCESS_MESSAGES["ban"],
                description=f"**ผู้ใช้:** {member.mention}\n**เหตุผล:** {reason}",
                color=discord.Color.dark_red()
            )
            embed.set_footer(text=f"ดำเนินการโดย {ctx.author.name}")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(config.ERROR_MESSAGES["bot_permission"])
        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    @commands.command(name="clear", description="ลบข้อความ")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """คำสั่งลบข้อความ"""
        if amount < 1 or amount > 100:
            await ctx.send(config.ERROR_MESSAGES["invalid_amount"])
            return

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 เพื่อลบข้อความคำสั่งด้วย
            embed = discord.Embed(
                title=config.SUCCESS_MESSAGES["clear"],
                description=f"ลบข้อความไปแล้ว {len(deleted)-1} ข้อความ",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"ดำเนินการโดย {ctx.author.name}")
            await ctx.send(embed=embed, delete_after=5)
        except discord.Forbidden:
            await ctx.send(config.ERROR_MESSAGES["bot_permission"])
        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    @commands.command(name="timeout", description="ระงับผู้ใช้ชั่วคราว")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason: str = "ไม่มีเหตุผล"):
        """คำสั่งระงับผู้ใช้ชั่วคราว"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send(config.ERROR_MESSAGES["role_hierarchy"])
            return

        if minutes < 1 or minutes > 40320:  # 28 วัน
            await ctx.send(config.ERROR_MESSAGES["invalid_time"])
            return

        try:
            duration = datetime.timedelta(minutes=minutes)
            await member.timeout(duration, reason=f"ระงับโดย {ctx.author.name}: {reason}")
            embed = discord.Embed(
                title=config.SUCCESS_MESSAGES["timeout"],
                description=f"**ผู้ใช้:** {member.mention}\n**เวลา:** {minutes} นาที\n**เหตุผล:** {reason}",
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"ดำเนินการโดย {ctx.author.name}")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(config.ERROR_MESSAGES["bot_permission"])
        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

    @kick.error
    @ban.error
    @clear.error
    @timeout.error
    async def moderation_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(config.ERROR_MESSAGES["missing_permissions"])
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(config.ERROR_MESSAGES["missing_arguments"])
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(config.ERROR_MESSAGES["member_not_found"])
        else:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(error)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot)) 