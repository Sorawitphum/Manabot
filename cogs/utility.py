import discord
from discord.ext import commands
from discord import app_commands
import datetime
import platform
import psutil
import time
import config

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="commands", description="แสดงรายการคำสั่งทั้งหมด")
    async def help_command(self, ctx):
        """คำสั่งแสดงรายการคำสั่งทั้งหมด"""
        embed = discord.Embed(
            title="📚 รายการคำสั่งทั้งหมด",
            description="คำสั่งทั้งหมดของบอท\nใช้ `!` นำหน้าทุกคำสั่ง\n\n**ตัวอย่าง:** `!ping`",
            color=discord.Color.blue()
        )
        
        # คำสั่งทั่วไป
        general = """
        `!ping` - ตรวจสอบการตอบสนองของบอท
        `!invite` - รับลิงก์เชิญบอท
        `!support` - รับลิงก์เซิร์ฟเวอร์สนับสนุน
        `!vote` - โหวตให้บอท
        `!donate` - สนับสนุนผู้พัฒนา
        """
        embed.add_field(
            name="🏠 คำสั่งทั่วไป",
            value=general,
            inline=False
        )
        
        # คำสั่งสนุก
        fun = """
        `!diceroll [จำนวน]` - สุ่มตัวเลข 1 ถึงจำนวนที่ระบุ
        `!pick ตัวเลือก1,ตัวเลือก2,...` - สุ่มเลือกจากตัวเลือกที่ให้มา
        `!flip` - โยนเหรียญ
        `!ask [คำถาม]` - ถามคำถามกับ 8ball
        `!dice [จำนวน]` - ทอยเต๋า 1-5 ลูก
        `!rps [ค้อน/กระดาษ/กรรไกร]` - เล่นเป่ายิ้งฉุบ
        `!random [min] [max]` - สุ่มตัวเลขระหว่างค่าที่กำหนด
        `!roll [จำนวน]` - สุ่มตัวเลข 1 ถึงจำนวนที่ระบุ
        `!choose ตัวเลือก1,ตัวเลือก2,...` - สุ่มเลือกจากตัวเลือกที่ให้มา
        `!coinflip` - โยนเหรียญ
        `!8ball [คำถาม]` - ถามคำถามกับ 8ball
        """
        embed.add_field(
            name="🎮 คำสั่งสนุก",
            value=fun,
            inline=False
        )
        
        # คำสั่งข้อมูล
        info = """
        `!userinfo [@ผู้ใช้]` - ดูข้อมูลผู้ใช้
        `!serverinfo` - ดูข้อมูลเซิร์ฟเวอร์
        `!roleinfo [@บทบาท]` - ดูข้อมูลบทบาท
        `!avatar [@ผู้ใช้]` - ดูรูปโปรไฟล์ผู้ใช้
        `!user [@ผู้ใช้]` - ดูข้อมูลผู้ใช้
        """
        embed.add_field(
            name="ℹ️ คำสั่งข้อมูล",
            value=info,
            inline=False
        )
        
        # คำสั่งจัดการ
        moderation = """
        `!kick [@ผู้ใช้] [เหตุผล]` - เตะผู้ใช้ออกจากเซิร์ฟเวอร์
        `!ban [@ผู้ใช้] [เหตุผล]` - แบนผู้ใช้จากเซิร์ฟเวอร์
        `!clear [จำนวน]` - ลบข้อความ
        `!timeout [@ผู้ใช้] [นาที] [เหตุผล]` - ระงับผู้ใช้ชั่วคราว
        """
        embed.add_field(
            name="🛡️ คำสั่งจัดการ",
            value=moderation,
            inline=False
        )

        # ระบบป้องกันสแปม
        spam_protection = """
        `!spamconfig<setting><value>` - ตั้งค่าระบบป้องกันสแปม
        `!spamstatus` - แสดงสถานะการตั้งค่า
        `!spamreset` - รีเซ็ตประวัติการเตือน
        `!spampatterns` - แสดงรูปแบบข้อความสแปม
        `!spamadd<pattern>` - เพิ่มรูปแบบข้อความสแปม
        `!spamremove<pattern>` - ลบรูปแบบข้อความสแปม

        **การตั้งค่าที่มี:**
        - `message_limit` - จำนวนข้อความสูงสุดที่อนุญาต
        - `time_window` - ระยะเวลา (วินาที)
        - `mute_duration` - ระยะเวลาลงโทษ (วินาที)
        - `warning_limit` - จำนวนครั้งสูงสุดที่เตือนก่อนเตะ
        - `warning_reset` - ระยะเวลารีเซ็ตการเตือน (วินาที)
        """
        embed.add_field(
            name="🛡️ ระบบป้องกันสแปม",
            value=spam_protection,
            inline=False
        )

        # ระบบ Ticket
        ticket = """
        `!ticket [เหตุผล]` - สร้าง ticket สำหรับติดต่อทีมงาน
        """
        embed.add_field(
            name="🎫 ระบบ Ticket",
            value=ticket,
            inline=False
        )

        # ระบบ Auto Role
        autorole = """
        `!autorole [@บทบาท]` - ตั้งค่าบทบาทอัตโนมัติสำหรับสมาชิกใหม่
        """
        embed.add_field(
            name="👥 ระบบ Auto Role",
            value=autorole,
            inline=False
        )

        # คำสั่งอื่นๆ
        other = """
        `!poll [คำถาม] [ตัวเลือก1,ตัวเลือก2,...]` - สร้างโพลแบบง่าย
        """
        embed.add_field(
            name="🔧 คำสั่งอื่นๆ",
            value=other,
            inline=False
        )

        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="info", description="แสดงข้อมูลบอท")
    async def info(self, ctx):
        """คำสั่งแสดงข้อมูลบอท"""
        # คำนวณเวลาทำงาน
        uptime = int(time.time() - self.start_time)
        days = uptime // 86400
        hours = (uptime % 86400) // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        # ข้อมูลระบบ
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        embed = discord.Embed(
            title="🤖 ข้อมูลบอท",
            color=discord.Color.blue()
        )
        
        # ข้อมูลทั่วไป
        embed.add_field(
            name="📊 ข้อมูลทั่วไป",
            value=f"""
            **ชื่อบอท:** {self.bot.user.name}
            **ID:** {self.bot.user.id}
            **เวอร์ชัน:** 1.0.0
            **Python:** {platform.python_version()}
            **Discord.py:** {discord.__version__}
            """,
            inline=False
        )
        
        # ข้อมูลเซิร์ฟเวอร์
        embed.add_field(
            name="🌐 ข้อมูลเซิร์ฟเวอร์",
            value=f"""
            **จำนวนเซิร์ฟเวอร์:** {len(self.bot.guilds)}
            **จำนวนผู้ใช้:** {sum(g.member_count for g in self.bot.guilds)}
            **จำนวนช่อง:** {sum(len(g.channels) for g in self.bot.guilds)}
            """,
            inline=False
        )
        
        # ข้อมูลระบบ
        embed.add_field(
            name="💻 ข้อมูลระบบ",
            value=f"""
            **CPU:** {cpu_usage}%
            **RAM:** {memory_usage}%
            **เวลาทำงาน:** {days} วัน {hours} ชั่วโมง {minutes} นาที {seconds} วินาที
            """,
            inline=False
        )
        
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="avatar", description="แสดงรูปโปรไฟล์ผู้ใช้")
    async def avatar(self, ctx, member: discord.Member = None):
        """คำสั่งแสดงรูปโปรไฟล์ผู้ใช้"""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"🖼️ รูปโปรไฟล์ของ {member.name}",
            color=discord.Color.blue()
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="roleinfo", description="แสดงข้อมูลบทบาท")
    async def roleinfo(self, ctx, role: discord.Role):
        """คำสั่งแสดงข้อมูลบทบาท"""
        # สร้างรายการสิทธิ์
        permissions = []
        for perm, value in role.permissions:
            if value:
                permissions.append(f"✅ {perm}")
            else:
                permissions.append(f"❌ {perm}")
        
        embed = discord.Embed(
            title=f"👑 ข้อมูลบทบาท: {role.name}",
            color=role.color
        )
        
        embed.add_field(
            name="📊 ข้อมูลทั่วไป",
            value=f"""
            **ID:** {role.id}
            **สี:** {role.color}
            **ตำแหน่ง:** {role.position}
            **แยกแสดง:** {'ใช่' if role.hoist else 'ไม่'}
            **กล่าวถึงได้:** {'ใช่' if role.mentionable else 'ไม่'}
            **สร้างเมื่อ:** {role.created_at.strftime('%d/%m/%Y %H:%M:%S')}
            """,
            inline=False
        )
        
        embed.add_field(
            name="👥 สิทธิ์",
            value="\n".join(permissions[:10]) + ("\n..." if len(permissions) > 10 else ""),
            inline=False
        )
        
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", description="แสดงข้อมูลเซิร์ฟเวอร์")
    async def server(self, ctx):
        """คำสั่งแสดงข้อมูลเซิร์ฟเวอร์"""
        guild = ctx.guild
        
        # สร้างรายการช่อง
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # สร้างรายการบทบาท
        roles = [role.mention for role in guild.roles[1:]]  # ไม่รวม @everyone
        roles_text = ", ".join(roles) if len(roles) <= 10 else ", ".join(roles[:10]) + "..."
        
        embed = discord.Embed(
            title=f"🌐 ข้อมูลเซิร์ฟเวอร์: {guild.name}",
            color=discord.Color.blue()
        )
        
        # ข้อมูลทั่วไป
        embed.add_field(
            name="📊 ข้อมูลทั่วไป",
            value=f"""
            **ID:** {guild.id}
            **เจ้าของ:** {guild.owner.mention}
            **สร้างเมื่อ:** {guild.created_at.strftime('%d/%m/%Y %H:%M:%S')}
            **ภูมิภาค:** {guild.region if hasattr(guild, 'region') else 'N/A'}
            """,
            inline=False
        )
        
        # ข้อมูลสมาชิก
        embed.add_field(
            name="👥 สมาชิก",
            value=f"""
            **ทั้งหมด:** {guild.member_count}
            **ผู้ใช้:** {len([m for m in guild.members if not m.bot])}
            **บอท:** {len([m for m in guild.members if m.bot])}
            """,
            inline=False
        )
        
        # ข้อมูลช่อง
        embed.add_field(
            name="📝 ช่อง",
            value=f"""
            **ข้อความ:** {text_channels}
            **เสียง:** {voice_channels}
            **หมวดหมู่:** {categories}
            """,
            inline=False
        )
        
        # ข้อมูลบทบาท
        embed.add_field(
            name="👑 บทบาท",
            value=roles_text,
            inline=False
        )
        
        # ไอคอนเซิร์ฟเวอร์
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", description="แสดงข้อมูลผู้ใช้")
    async def user(self, ctx, member: discord.Member = None):
        """คำสั่งแสดงข้อมูลผู้ใช้"""
        member = member or ctx.author
        
        # สร้างรายการบทบาท
        roles = [role.mention for role in member.roles[1:]]  # ไม่รวม @everyone
        roles_text = ", ".join(roles) if len(roles) <= 10 else ", ".join(roles[:10]) + "..."
        
        embed = discord.Embed(
            title=f"👤 ข้อมูลผู้ใช้: {member.name}",
            color=member.color
        )
        
        # ข้อมูลทั่วไป
        embed.add_field(
            name="📊 ข้อมูลทั่วไป",
            value=f"""
            **ID:** {member.id}
            **ชื่อ:** {member.name}
            **ชื่อเล่น:** {member.nick if member.nick else 'ไม่มี'}
            **บอท:** {'ใช่' if member.bot else 'ไม่'}
            **บัญชีสร้างเมื่อ:** {member.created_at.strftime('%d/%m/%Y %H:%M:%S')}
            **เข้าร่วมเมื่อ:** {member.joined_at.strftime('%d/%m/%Y %H:%M:%S')}
            """,
            inline=False
        )
        
        # ข้อมูลบทบาท
        embed.add_field(
            name="👑 บทบาท",
            value=roles_text,
            inline=False
        )
        
        # รูปโปรไฟล์
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot)) 