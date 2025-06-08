import discord
from discord.ext import commands
import time
from collections import defaultdict
import re
import logging

class SpamProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        # เก็บข้อมูลการส่งข้อความของผู้ใช้
        self.message_history = defaultdict(list)
        # ตั้งค่าการป้องกันสแปม
        self.spam_settings = {
            'message_limit': 5,  # จำนวนข้อความสูงสุดที่อนุญาต
            'time_window': 5,    # ระยะเวลา (วินาที)
            'mute_duration': 300 # ระยะเวลาลงโทษ (วินาที)
        }
        # รูปแบบข้อความสแปม
        self.spam_patterns = [
            r'(?i)(?:http|https)://',  # ลิงก์
            r'(?i)(?:discord\.gg|discord\.com/invite)',  # ลิงก์เชิญ Discord
            r'(?i)(?:@everyone|@here)',  # การแท็กทุกคน
            r'(?i)(?:free|nitro|gift)',  # คำที่มักใช้ในการสแปม
            r'(?i)(?:gay|fuck|shit|bitch)',  # คำหยาบ
        ]
        self.logger.info("Spam Protection system initialized")

    def is_spam_message(self, message):
        """ตรวจสอบว่าข้อความเป็นสแปมหรือไม่"""
        # ตรวจสอบรูปแบบข้อความสแปม
        for pattern in self.spam_patterns:
            if re.search(pattern, message.content):
                self.logger.info(f"Spam detected: {message.content}")
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        # ข้ามข้อความจากบอท
        if message.author.bot:
            return

        # ตรวจสอบสิทธิ์การจัดการ
        if message.author.guild_permissions.manage_messages:
            return

        try:
            # เก็บข้อมูลข้อความ
            user_id = message.author.id
            current_time = time.time()
            
            # เพิ่มข้อความใหม่
            self.message_history[user_id].append(current_time)
            
            # ลบข้อความเก่าที่อยู่นอกหน้าต่างเวลา
            self.message_history[user_id] = [
                t for t in self.message_history[user_id]
                if current_time - t <= self.spam_settings['time_window']
            ]

            # ตรวจสอบการสแปม
            if len(self.message_history[user_id]) > self.spam_settings['message_limit']:
                self.logger.info(f"Rate limit exceeded for user {user_id}")
                # ลบข้อความสแปม
                try:
                    await message.delete()
                    self.logger.info(f"Deleted spam message from user {user_id}")
                except discord.Forbidden:
                    self.logger.error(f"Cannot delete message: Missing permissions")
                    return
                
                # ลงโทษผู้ใช้
                try:
                    # ลองใช้ timeout ก่อน
                    await message.author.timeout(
                        duration=self.spam_settings['mute_duration'],
                        reason="Spam Protection: Message Rate Limit Exceeded"
                    )
                    await message.channel.send(
                        f"⚠️ {message.author.mention} ถูกระงับการใช้งานชั่วคราวเนื่องจากส่งข้อความเร็วเกินไป",
                        delete_after=10
                    )
                    self.logger.info(f"User {user_id} has been timed out")
                except discord.Forbidden:
                    # ถ้าไม่มีสิทธิ์ timeout ให้เตะออก
                    try:
                        await message.author.kick(reason="Spam Protection: Message Rate Limit Exceeded")
                        await message.channel.send(
                            f"⚠️ {message.author.mention} ถูกเตะออกเนื่องจากส่งข้อความเร็วเกินไป",
                            delete_after=10
                        )
                        self.logger.info(f"User {user_id} has been kicked")
                    except discord.Forbidden:
                        await message.channel.send(
                            "❌ ไม่สามารถจัดการผู้ใช้ที่สแปมได้ กรุณาตรวจสอบสิทธิ์ของบอท",
                            delete_after=10
                        )
                        self.logger.error(f"Cannot manage user: Missing permissions")

            # ตรวจสอบเนื้อหาข้อความ
            if self.is_spam_message(message):
                self.logger.info(f"Spam content detected from user {user_id}")
                # ลบข้อความสแปม
                try:
                    await message.delete()
                    self.logger.info(f"Deleted spam message from user {user_id}")
                except discord.Forbidden:
                    self.logger.error(f"Cannot delete message: Missing permissions")
                    return
                
                # แจ้งเตือน
                try:
                    await message.author.timeout(
                        duration=self.spam_settings['mute_duration'],
                        reason="Spam Protection: Spam Content Detected"
                    )
                    await message.channel.send(
                        f"⚠️ {message.author.mention} ถูกระงับการใช้งานชั่วคราวเนื่องจากส่งข้อความสแปม",
                        delete_after=10
                    )
                    self.logger.info(f"User {user_id} has been timed out")
                except discord.Forbidden:
                    try:
                        await message.author.kick(reason="Spam Protection: Spam Content Detected")
                        await message.channel.send(
                            f"⚠️ {message.author.mention} ถูกเตะออกเนื่องจากส่งข้อความสแปม",
                            delete_after=10
                        )
                        self.logger.info(f"User {user_id} has been kicked")
                    except discord.Forbidden:
                        await message.channel.send(
                            "❌ ไม่สามารถจัดการผู้ใช้ที่สแปมได้ กรุณาตรวจสอบสิทธิ์ของบอท",
                            delete_after=10
                        )
                        self.logger.error(f"Cannot manage user: Missing permissions")

        except Exception as e:
            self.logger.error(f"Error in spam protection: {e}")

    @commands.command(name="spamconfig")
    @commands.has_permissions(administrator=True)
    async def spam_config(self, ctx, setting: str, value: int):
        """ตั้งค่าระบบป้องกันสแปม"""
        try:
            if setting not in self.spam_settings:
                await ctx.send("❌ การตั้งค่าไม่ถูกต้อง\nการตั้งค่าที่มี: message_limit, time_window, mute_duration")
                return

            if value < 1:
                await ctx.send("❌ ค่าต้องมากกว่า 0")
                return

            self.spam_settings[setting] = value
            await ctx.send(f"✅ ตั้งค่า {setting} เป็น {value} เรียบร้อยแล้ว")
            self.logger.info(f"Spam protection setting updated: {setting} = {value}")
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการตั้งค่า กรุณาลองใหม่อีกครั้ง")
            self.logger.error(f"Error in spam config: {e}")

async def setup(bot):
    await bot.add_cog(SpamProtection(bot))
    logging.info("Spam Protection cog loaded successfully") 