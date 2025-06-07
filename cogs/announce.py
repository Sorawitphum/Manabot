import discord
from discord import app_commands
from discord.ext import commands
import datetime
import logging
import config
from typing import Optional, List
import asyncio
import os

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.logger.info("เริ่มต้นระบบประกาศ")

    def get_icon_path(self, icon_name: str) -> Optional[str]:
        """หา path ของไอคอนในโฟลเดอร์ assets"""
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        icon_path = os.path.join(assets_dir, icon_name)
        if os.path.exists(icon_path):
            return icon_path
        return None

    @app_commands.command(
        name="announce",
        description="ส่งประกาศไปยังช่องที่เลือก"
    )
    @app_commands.describe(
        channel="ช่องที่จะส่งประกาศ",
        message="ข้อความที่จะประกาศ",
        color="สีของ embed (hex code เช่น #FF0000)",
        template="รูปแบบการประกาศ",
        schedule="เวลาที่จะประกาศ (เช่น 2024-03-08 23:00)"
    )
    @app_commands.choices(template=[
        app_commands.Choice(name=template_name, value=template_name)
        for template_name in config.ANNOUNCEMENT_TEMPLATES.keys()
    ])
    async def announce(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str,
        template: str = "normal",
        color: Optional[str] = None,
        schedule: Optional[str] = None
    ):
        """ส่งประกาศไปยังช่องที่เลือก"""
        # ตรวจสอบสิทธิ์
        user_roles = [role.name for role in interaction.user.roles]
        allowed_roles = [role for role in config.ANNOUNCEMENT_ROLES if role in user_roles]
        
        if not allowed_roles:
            await interaction.response.send_message(
                f"❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้ ต้องมีบทบาท {', '.join(config.ANNOUNCEMENT_ROLES)} เท่านั้น",
                ephemeral=True
            )
            return

        try:
            # สร้าง embed
            template_data = config.ANNOUNCEMENT_TEMPLATES[template]
            
            # จัดการสี
            if color:
                try:
                    embed_color = int(color.replace("#", ""), 16)
                except ValueError:
                    await interaction.response.send_message("❌ รูปแบบสีไม่ถูกต้อง ใช้รูปแบบ #RRGGBB", ephemeral=True)
                    return
            else:
                try:
                    embed_color = int(template_data["color"].replace("#", ""), 16)
                except (ValueError, AttributeError):
                    embed_color = 0x3498db  # สีฟ้าเป็นค่าเริ่มต้น

            embed = discord.Embed(
                title=template_data["title"],
                description=message,
                color=embed_color,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f"ประกาศโดย {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
            
            # เพิ่ม thumbnail จากไฟล์ในโฟลเดอร์ assets
            icon_path = self.get_icon_path(template_data["icon"])
            
            # จัดการการตั้งเวลา
            if schedule:
                try:
                    schedule_time = datetime.datetime.strptime(schedule, "%Y-%m-%d %H:%M")
                    if schedule_time < datetime.datetime.now():
                        await interaction.response.send_message("❌ ไม่สามารถตั้งเวลาย้อนหลังได้", ephemeral=True)
                        return
                    
                    # ส่งข้อความยืนยันการตั้งเวลา
                    await interaction.response.send_message(
                        f"✅ จะส่งประกาศในช่อง {channel.mention} เมื่อถึงเวลา {schedule}",
                        ephemeral=True
                    )
                    
                    # คำนวณเวลาที่ต้องรอ
                    wait_seconds = (schedule_time - datetime.datetime.now()).total_seconds()
                    
                    # รอจนถึงเวลาที่กำหนด
                    await asyncio.sleep(wait_seconds)
                    
                    # ส่งประกาศเมื่อถึงเวลา
                    if icon_path:
                        file = discord.File(icon_path, filename=template_data["icon"])
                        embed.set_thumbnail(url=f"attachment://{template_data['icon']}")
                        await channel.send(embed=embed, file=file)
                    else:
                        await channel.send(embed=embed)
                        
                except ValueError:
                    await interaction.response.send_message(
                        "❌ รูปแบบเวลาไม่ถูกต้อง ใช้รูปแบบ YYYY-MM-DD HH:MM",
                        ephemeral=True
                    )
                    return
            else:
                # ส่งประกาศทันที
                await interaction.response.send_message(
                    f"✅ ส่งประกาศไปยังช่อง {channel.mention} แล้ว",
                    ephemeral=True
                )
                
                if icon_path:
                    file = discord.File(icon_path, filename=template_data["icon"])
                    embed.set_thumbnail(url=f"attachment://{template_data['icon']}")
                    await channel.send(embed=embed, file=file)
                else:
                    await channel.send(embed=embed)

            # บันทึกการใช้งาน
            if config.ANNOUNCEMENT_LOG_CHANNEL_ID:
                log_channel = self.bot.get_channel(config.ANNOUNCEMENT_LOG_CHANNEL_ID)
                if log_channel:
                    log_embed = discord.Embed(
                        title="📢 บันทึกการประกาศ",
                        color=discord.Color.blue(),
                        timestamp=datetime.datetime.now()
                    )
                    log_embed.add_field(name="ผู้ประกาศ", value=interaction.user.mention, inline=True)
                    log_embed.add_field(name="ช่อง", value=channel.mention, inline=True)
                    log_embed.add_field(name="รูปแบบ", value=template_data["title"], inline=True)
                    if schedule:
                        log_embed.add_field(name="เวลาที่ส่ง", value=schedule, inline=True)
                    log_embed.add_field(name="ข้อความ", value=message, inline=False)
                    await log_channel.send(embed=log_embed)

        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการส่งประกาศ: {e}")
            await interaction.response.send_message("❌ เกิดข้อผิดพลาดในการส่งประกาศ", ephemeral=True)

    @app_commands.command(
        name="announcement",
        description="ดูคำสั่งและวิธีการใช้งานระบบประกาศ"
    )
    async def announcement_help(self, interaction: discord.Interaction):
        """แสดงคำสั่งและวิธีการใช้งานระบบประกาศ"""
        embed = discord.Embed(
            title="📢 ระบบประกาศ",
            description="คำสั่งและวิธีการใช้งานระบบประกาศ",
            color=discord.Color.blue()
        )

        # แสดงคำสั่งหลัก
        embed.add_field(
            name="📝 คำสั่งหลัก",
            value="`/announce` - ส่งประกาศไปยังช่องที่เลือก",
            inline=False
        )

        # แสดงพารามิเตอร์
        embed.add_field(
            name="⚙️ พารามิเตอร์",
            value="""
`channel` - ช่องที่จะส่งประกาศ
`message` - ข้อความที่จะประกาศ
`color` - สีของ embed (hex code เช่น #FF0000)
`template` - รูปแบบการประกาศ
`schedule` - เวลาที่จะประกาศ (เช่น 2024-03-08 23:00)
            """,
            inline=False
        )

        # แสดงรูปแบบการประกาศ
        templates = "\n".join([
            f"• {template['title']} - {template_name}"
            for template_name, template in config.ANNOUNCEMENT_TEMPLATES.items()
        ])
        embed.add_field(
            name="🎨 รูปแบบการประกาศ",
            value=templates,
            inline=False
        )

        # แสดงตัวอย่างการใช้งาน
        embed.add_field(
            name="📚 ตัวอย่างการใช้งาน",
            value="""
1. `/announce channel:#ประกาศ message:"เซิร์ฟเวอร์จะปิดปรับปรุงคืนนี้ 23.00 น." template:warning`
2. `/announce channel:#ข่าวสาร message:"มีกิจกรรมใหม่!" template:event color:#FF0000`
3. `/announce channel:#ประกาศ message:"ประกาศล่วงหน้า" template:normal schedule:2024-03-08 23:00`
            """,
            inline=False
        )

        # แสดงข้อจำกัด
        embed.add_field(
            name="⚠️ ข้อจำกัด",
            value=f"ต้องมีบทบาท {', '.join(config.ANNOUNCEMENT_ROLES)} เท่านั้น",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announce(bot))
    logging.info("ตั้งค่าระบบประกาศเสร็จสมบูรณ์") 