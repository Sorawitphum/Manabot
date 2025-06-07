import discord
from discord.ext import commands
import datetime
import config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="latency", description="ตรวจสอบการตอบสนองของบอท")
    async def ping(self, ctx):
        """คำสั่งตรวจสอบการตอบสนองของบอท"""
        embed = discord.Embed(
            title="🏓 ปิง",
            description=f"ความเร็วในการตอบสนอง: {round(self.bot.latency * 1000)}ms",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="invite", description="แสดงลิงก์เชิญบอท")
    async def invite(self, ctx):
        """คำสั่งแสดงลิงก์เชิญบอท"""
        embed = discord.Embed(
            title="🔗 เชิญบอท",
            description="[คลิกที่นี่เพื่อเชิญบอท](https://discord.com/oauth2/authorize?client_id=1380811709358411868&permissions=0&integration_type=0&scope=bot)",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="support", description="แสดงลิงก์เซิร์ฟเวอร์สนับสนุน")
    async def support(self, ctx):
        """คำสั่งแสดงลิงก์เซิร์ฟเวอร์สนับสนุน"""
        if not config.SUPPORT_SERVER_LINK or config.SUPPORT_SERVER_LINK == "YOUR_SUPPORT_SERVER_INVITE_LINK":
            await ctx.send("❌ ยังไม่ได้ตั้งค่าลิงก์เซิร์ฟเวอร์สนับสนุน กรุณาติดต่อผู้ดูแลระบบ")
            return

        embed = discord.Embed(
            title="💬 เซิร์ฟเวอร์สนับสนุน",
            description=f"[คลิกที่นี่เพื่อเข้าร่วมเซิร์ฟเวอร์สนับสนุน]({config.SUPPORT_SERVER_LINK})", 
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="vote", description="โหวตให้บอท")
    async def vote(self, ctx):
        """คำสั่งโหวตให้บอท"""
        embed = discord.Embed(
            title="⭐ โหวตให้บอท",
            description="[คลิกที่นี่เพื่อโหวตให้บอท](YOUR_VOTE_LINK)",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def donate(self, ctx):
        embed = discord.Embed(
            title="☕ สนับสนุนผู้พัฒนา",
            description="หากคุณชื่นชอบบอทนี้ สามารถสนับสนุนผู้พัฒนาได้ทาง QR ด้านล่างนี้ ❤️\n\n**ขอบคุณสำหรับน้ำใจ!**",
            color=discord.Color.green()
        )   
        file = discord.File("./assets/donate_qr.jpg", filename="donate_qr.jpg")
        embed.set_image(url="attachment://donate_qr.jpg")
        await ctx.send(embed=embed, file=file)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def A(self, ctx, *, message: str):
        await ctx.send(f'📢 **ประกาศจากแอดมิน:** {message}')

async def setup(bot):
    await bot.add_cog(General(bot))
