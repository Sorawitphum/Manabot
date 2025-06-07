from discord.ext import commands
import random
import aiohttp
import discord

bad_words = ["คำหยาบ", "โง่", "ควาย", "เหี้ย"]

class Filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for word in bad_words:
            if word in message.content:
                await message.delete()
                await message.channel.send(f"{message.author.mention} 🚫 กรุณาอย่าใช้คำไม่สุภาพ")
                break

    @commands.command(name="roll")
    async def roll(self, ctx, max_number: int = 100):
        """คำสั่งสุ่มตัวเลข"""
        if max_number < 1:
            await ctx.send("❌ กรุณาระบุตัวเลขที่มากกว่า 0")
            return
        
        number = random.randint(1, max_number)
        embed = discord.Embed(
            title="🎲 สุ่มตัวเลข",
            description=f"คุณได้เลข: **{number}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name="choose")
    async def choose(self, ctx, *, choices: str):
        """คำสั่งสุ่มเลือกจากตัวเลือกที่ให้มา"""
        choices_list = choices.split(',')
        if len(choices_list) < 2:
            await ctx.send("❌ กรุณาระบุตัวเลือกอย่างน้อย 2 ตัวเลือก (คั่นด้วยเครื่องหมาย ,)")
            return
        
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="🤔 สุ่มเลือก",
            description=f"ตัวเลือกทั้งหมด: {', '.join(choices_list)}\n\nผลลัพธ์: **{choice}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="coinflip")
    async def coinflip(self, ctx):
        """คำสั่งโยนเหรียญ"""
        result = random.choice(["หัว", "ก้อย"])
        embed = discord.Embed(
            title="🪙 โยนเหรียญ",
            description=f"ผลลัพธ์: **{result}**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question: str):
        """คำสั่งถามคำถามกับ 8ball"""
        responses = [
            "แน่นอนครับ", "แน่นอนค่ะ", "ใช่ครับ", "ใช่ค่ะ",
            "ไม่แน่นอนครับ", "ไม่แน่นอนค่ะ", "ไม่ใช่ครับ", "ไม่ใช่ค่ะ",
            "ลองถามใหม่นะครับ", "ลองถามใหม่นะค่ะ",
            "บอกไม่ได้ตอนนี้ครับ", "บอกไม่ได้ตอนนี้ค่ะ",
            "คาดเดาไม่ได้ครับ", "คาดเดาไม่ได้ค่ะ",
            "สัญญาณบอกว่าใช่ครับ", "สัญญาณบอกว่าใช่ค่ะ",
            "สัญญาณบอกว่าไม่ครับ", "สัญญาณบอกว่าไม่ค่ะ"
        ]
        
        embed = discord.Embed(
            title="🎱 8ball",
            description=f"คำถาม: {question}\nคำตอบ: **{random.choice(responses)}**",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="server")
    async def serverinfo(self, ctx):
        """คำสั่งแสดงข้อมูลของเซิร์ฟเวอร์"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 ข้อมูลเซิร์ฟเวอร์ {guild.name}",
            color=discord.Color.blue()
        )
        
        # ข้อมูลพื้นฐาน
        embed.add_field(name="👑 เจ้าของเซิร์ฟเวอร์", value=guild.owner.mention, inline=True)
        embed.add_field(name="👥 จำนวนสมาชิก", value=guild.member_count, inline=True)
        embed.add_field(name="📅 สร้างเมื่อ", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        
        # ข้อมูลช่อง
        embed.add_field(name="💬 จำนวนช่องข้อความ", value=len(guild.text_channels), inline=True)
        embed.add_field(name="🔊 จำนวนช่องเสียง", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="🎭 จำนวนบทบาท", value=len(guild.roles), inline=True)
        
        # ไอคอนเซิร์ฟเวอร์
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="user")
    async def userinfo(self, ctx, member: discord.Member = None):
        """คำสั่งแสดงข้อมูลของผู้ใช้"""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"👤 ข้อมูลผู้ใช้ {member.name}",
            color=member.color
        )
        
        # ข้อมูลพื้นฐาน
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📅 เข้าร่วมเมื่อ", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="📅 สร้างบัญชีเมื่อ", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        
        # บทบาท
        roles = [role.mention for role in member.roles[1:]]  # ไม่รวม @everyone
        if roles:
            embed.add_field(name="บทบาท", value=" ".join(roles), inline=False)
        
        # อวาตาร์
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """คำสั่งแสดงความเร็วในการตอบสนองของบอท"""
        embed = discord.Embed(
            title="🏓 ปิง",
            description=f"ความเร็วในการตอบสนอง: {round(self.bot.latency * 1000)}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, ctx, question: str, *, options: str):
        """คำสั่งสร้างโพลแบบง่าย"""
        options_list = options.split(',')
        if len(options_list) < 2:
            await ctx.send("❌ กรุณาระบุตัวเลือกอย่างน้อย 2 ตัวเลือก (คั่นด้วยเครื่องหมาย ,)")
            return
        
        if len(options_list) > 10:
            await ctx.send("❌ ไม่สามารถมีตัวเลือกได้มากกว่า 10 ตัวเลือก")
            return
        
        # สร้าง embed สำหรับโพล
        embed = discord.Embed(
            title="📊 โพล",
            description=question,
            color=discord.Color.blue()
        )
        
        # เพิ่มตัวเลือกและ emoji
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for idx, option in enumerate(options_list):
            embed.add_field(name=f"{emojis[idx]} {option}", value="", inline=False)
        
        # ส่งโพลและเพิ่มปฏิกิริยา
        poll_message = await ctx.send(embed=embed)
        for idx in range(len(options_list)):
            await poll_message.add_reaction(emojis[idx])

async def setup(bot):
    await bot.add_cog(Filter(bot))
