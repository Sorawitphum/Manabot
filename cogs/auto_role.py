import discord
from discord.ext import commands
import config

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ให้บทบาทอัตโนมัติเมื่อสมาชิกใหม่เข้าร่วม"""
        if not config.AUTO_ROLE["enabled"]:
            return

        try:
            for role_id in config.AUTO_ROLE["roles"]:
                role = member.guild.get_role(role_id)
                if role:
                    await member.add_roles(role)
                    print(f"✅ Gave role {role.name} to {member.name}")
        except Exception as e:
            print(f"❌ Failed to give auto role: {str(e)}")

    @commands.command(name="autorole", description="ตั้งค่าบทบาทอัตโนมัติ")
    @commands.has_permissions(administrator=True)
    async def set_auto_role(self, ctx, role: discord.Role):
        """คำสั่งตั้งค่าบทบาทอัตโนมัติ"""
        if role.id not in config.AUTO_ROLE["roles"]:
            config.AUTO_ROLE["roles"].append(role.id)
            embed = discord.Embed(
                title="✅ ตั้งค่าบทบาทอัตโนมัติ",
                description=f"เพิ่มบทบาท {role.mention} เป็นบทบาทอัตโนมัติ",
                color=discord.Color.green()
            )
        else:
            config.AUTO_ROLE["roles"].remove(role.id)
            embed = discord.Embed(
                title="✅ ลบบทบาทอัตโนมัติ",
                description=f"ลบบทบาท {role.mention} ออกจากบทบาทอัตโนมัติ",
                color=discord.Color.red()
            )
        
        embed.set_footer(text=f"ดำเนินการโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @set_auto_role.error
    async def set_auto_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(config.ERROR_MESSAGES["missing_permissions"])
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ กรุณาระบุบทบาทที่ต้องการตั้งค่า")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("❌ ไม่พบบทบาทที่ระบุ")
        else:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(error)}")

async def setup(bot):
    await bot.add_cog(AutoRole(bot)) 