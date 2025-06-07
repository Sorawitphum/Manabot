import discord
from discord import app_commands
from discord.ext import commands
import config
import datetime
import logging

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Help cog initialized")

    @app_commands.command(name="help", description="แสดงรายการคำสั่งทั้งหมด")
    async def help_command(self, interaction: discord.Interaction):
        """คำสั่งแสดงรายการคำสั่งทั้งหมด"""
        logging.info(f"Help command called by {interaction.user}")
        try:
            embed = discord.Embed(
                title="📚 รายการคำสั่งทั้งหมด",
                description="คำสั่งทั้งหมดของบอท\nใช้ `/` นำหน้าคำสั่ง slash commands\nใช้ `!` นำหน้าคำสั่งทั่วไป\n\n**ตัวอย่าง:** `/help` หรือ `!ping`",
                color=discord.Color.blue()
            )
            
            # คำสั่งทั่วไป
            general = """
            `/help` - แสดงรายการคำสั่งทั้งหมด
            `/feedback [ข้อความ]` - ส่งข้อเสนอแนะหรือรายงานปัญหา
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
            
            # ระบบประกาศ
            announcement = """
            `/announce` - ส่งประกาศไปยังช่องที่เลือก
            `/announcement` - ดูคำสั่งและวิธีการใช้งานระบบประกาศ
            """
            embed.add_field(
                name="📢 ระบบประกาศ",
                value=announcement,
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

            embed.set_footer(text=f"คำขอโดย {interaction.user.name}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info("Help command response sent successfully")
        except Exception as e:
            logging.error(f"Error in help command: {e}")
            await interaction.response.send_message("❌ เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง", ephemeral=True)

    @app_commands.command(name="feedback", description="ส่งข้อเสนอแนะหรือรายงานปัญหา")
    @app_commands.describe(message="ข้อความที่ต้องการส่ง")
    async def feedback(self, interaction: discord.Interaction, message: str):
        """คำสั่งส่งข้อเสนอแนะหรือรายงานปัญหา"""
        logging.info(f"Feedback command called by {interaction.user} with message: {message}")
        try:
            # สร้าง embed สำหรับ feedback
            embed = discord.Embed(
                title="📝 ข้อเสนอแนะ/รายงานปัญหา",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            
            # เพิ่มข้อมูลผู้ส่ง
            embed.add_field(
                name="👤 ผู้ส่ง",
                value=f"{interaction.user.mention} (`{interaction.user.id}`)",
                inline=False
            )
            
            # เพิ่มข้อมูลเซิร์ฟเวอร์
            embed.add_field(
                name="🏠 เซิร์ฟเวอร์",
                value=f"{interaction.guild.name} (`{interaction.guild.id}`)",
                inline=False
            )
            
            # ส่ง feedback ไปยังช่องที่กำหนด
            if config.FEEDBACK_CHANNEL_ID:
                try:
                    feedback_channel = self.bot.get_channel(config.FEEDBACK_CHANNEL_ID)
                    if feedback_channel:
                        await feedback_channel.send(embed=embed)
                        await interaction.response.send_message("✅ ส่งข้อเสนอแนะ/รายงานปัญหาสำเร็จแล้ว ขอบคุณสำหรับความคิดเห็น!", ephemeral=True)
                        logging.info(f"Feedback sent to channel {config.FEEDBACK_CHANNEL_ID}")
                    else:
                        logging.error(f"Feedback channel {config.FEEDBACK_CHANNEL_ID} not found")
                        await interaction.response.send_message("❌ ไม่พบช่องสำหรับส่ง feedback กรุณาติดต่อผู้ดูแลระบบ", ephemeral=True)
                except Exception as e:
                    logging.error(f"Error sending feedback to channel: {e}")
                    await interaction.response.send_message("❌ เกิดข้อผิดพลาดในการส่ง feedback กรุณาลองใหม่อีกครั้ง", ephemeral=True)
            else:
                # ถ้าไม่มีช่อง feedback ให้ส่งไปหา owner
                owner = self.bot.get_user(self.bot.owner_id)
                if owner:
                    try:
                        await owner.send(embed=embed)
                        await interaction.response.send_message("✅ ส่งข้อเสนอแนะ/รายงานปัญหาสำเร็จแล้ว ขอบคุณสำหรับความคิดเห็น!", ephemeral=True)
                        logging.info("Feedback sent to bot owner")
                    except Exception as e:
                        logging.error(f"Error sending feedback to owner: {e}")
                        await interaction.response.send_message("❌ ไม่สามารถส่ง feedback ได้ กรุณาลองใหม่อีกครั้ง", ephemeral=True)
                else:
                    logging.error("Bot owner not found")
                    await interaction.response.send_message("❌ ไม่สามารถส่ง feedback ได้ กรุณาลองใหม่อีกครั้ง", ephemeral=True)
        except Exception as e:
            logging.error(f"Error in feedback command: {e}")
            await interaction.response.send_message("❌ เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
    logging.info("Help cog setup completed") 