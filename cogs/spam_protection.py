import discord
from discord.ext import commands
import time
from collections import defaultdict
import re
import logging
import asyncio

class SpamProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        # เก็บข้อมูลการส่งข้อความของผู้ใช้
        self.message_history = defaultdict(list)
        # เก็บประวัติการเตือนของผู้ใช้
        self.warning_history = defaultdict(int)
        # ตั้งค่าการป้องกันสแปม
        self.spam_settings = {
            'message_limit': 5,      # จำนวนข้อความสูงสุดที่อนุญาต
            'time_window': 5,        # ระยะเวลา (วินาที)
            'mute_duration': 300,    # ระยะเวลาลงโทษ (วินาที)
            'warning_limit': 3,      # จำนวนครั้งสูงสุดที่เตือนก่อนเตะ
            'warning_reset': 3600    # ระยะเวลารีเซ็ตการเตือน (วินาที)
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
        # เริ่มการรีเซ็ตการเตือนอัตโนมัติ
        self.bot.loop.create_task(self.reset_warnings())

    async def reset_warnings(self):
        """รีเซ็ตประวัติการเตือนทุกๆ warning_reset วินาที"""
        while True:
            await asyncio.sleep(self.spam_settings['warning_reset'])
            self.warning_history.clear()
            self.logger.info("Warning history has been reset")

    def is_spam_message(self, message):
        """ตรวจสอบว่าข้อความเป็นสแปมหรือไม่"""
        # ตรวจสอบรูปแบบข้อความสแปม
        for pattern in self.spam_patterns:
            if re.search(pattern, message.content):
                self.logger.info(f"Spam detected: {message.content}")
                return True
        return False

    async def send_warning(self, channel, user, reason):
        """ส่งข้อความเตือน"""
        try:
            embed = discord.Embed(
                title="⚠️ การเตือน",
                description=f"{user.mention} {reason}",
                color=discord.Color.red()
            )
            warning_msg = await channel.send(embed=embed)
            await warning_msg.delete(delay=10)  # ลบข้อความเตือนหลังจาก 10 วินาที
            self.logger.info(f"Warning sent to {user.id}: {reason}")
        except Exception as e:
            self.logger.error(f"Failed to send warning: {e}")

    async def handle_spam(self, message, reason):
        """จัดการกรณีสแปม"""
        user_id = message.author.id
        self.warning_history[user_id] += 1
        
        # ลบข้อความสแปม
        try:
            await message.delete()
            self.logger.info(f"Deleted spam message from user {user_id}")
        except discord.Forbidden:
            self.logger.error(f"Cannot delete message: Missing permissions")
            return

        # ตรวจสอบจำนวนครั้งที่เตือน
        if self.warning_history[user_id] >= self.spam_settings['warning_limit']:
            # เตะผู้ใช้ออก
            try:
                await message.author.kick(reason=f"Spam Protection: {reason}")
                await self.send_warning(
                    message.channel,
                    message.author,
                    f"ถูกเตะออกเนื่องจาก {reason}"
                )
                self.logger.info(f"User {user_id} has been kicked")
                self.warning_history[user_id] = 0
            except discord.Forbidden:
                await self.send_warning(
                    message.channel,
                    message.author,
                    "ไม่สามารถจัดการผู้ใช้ที่สแปมได้ กรุณาตรวจสอบสิทธิ์ของบอท"
                )
                self.logger.error(f"Cannot kick user: Missing permissions")
        else:
            # timeout ผู้ใช้
            try:
                await message.author.timeout(
                    duration=self.spam_settings['mute_duration'],
                    reason=f"Spam Protection: {reason}"
                )
                await self.send_warning(
                    message.channel,
                    message.author,
                    f"ถูกระงับการใช้งานชั่วคราวเนื่องจาก {reason}"
                )
                self.logger.info(f"User {user_id} has been timed out")
            except discord.Forbidden:
                await self.send_warning(
                    message.channel,
                    message.author,
                    "ไม่สามารถระงับการใช้งานได้ กรุณาตรวจสอบสิทธิ์ของบอท"
                )
                self.logger.error(f"Cannot timeout user: Missing permissions")

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
                await self.handle_spam(message, "ส่งข้อความเร็วเกินไป")
                return

            # ตรวจสอบเนื้อหาข้อความ
            if self.is_spam_message(message):
                self.logger.info(f"Spam content detected from user {user_id}")
                await self.handle_spam(message, "ส่งข้อความสแปม")
                return

        except Exception as e:
            self.logger.error(f"Error in spam protection: {e}")

    @commands.group(name="spam", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx):
        """คำสั่งจัดการระบบป้องกันสแปม"""
        embed = discord.Embed(
            title="🛡️ ระบบป้องกันสแปม",
            description="คำสั่งสำหรับจัดการระบบป้องกันสแปม",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="📝 คำสั่งพื้นฐาน",
            value=(
                "`!spam config <setting> <value>` - ตั้งค่าต่างๆ\n"
                "`!spam status` - แสดงสถานะการตั้งค่า\n"
                "`!spam reset` - รีเซ็ตประวัติการเตือน\n"
                "`!spam patterns` - แสดงรูปแบบข้อความสแปม\n"
                "`!spam add <pattern>` - เพิ่มรูปแบบข้อความสแปม\n"
                "`!spam remove <pattern>` - ลบรูปแบบข้อความสแปม"
            ),
            inline=False
        )
        embed.add_field(
            name="⚙️ การตั้งค่าที่มี",
            value=(
                "`message_limit` - จำนวนข้อความสูงสุดที่อนุญาต\n"
                "`time_window` - ระยะเวลา (วินาที)\n"
                "`mute_duration` - ระยะเวลาลงโทษ (วินาที)\n"
                "`warning_limit` - จำนวนครั้งสูงสุดที่เตือนก่อนเตะ\n"
                "`warning_reset` - ระยะเวลารีเซ็ตการเตือน (วินาที)"
            ),
            inline=False
        )
        await ctx.send(embed=embed)

    @spam.command(name="config")
    @commands.has_permissions(administrator=True)
    async def spam_config(self, ctx, setting: str, value: int):
        """ตั้งค่าระบบป้องกันสแปม"""
        try:
            if setting not in self.spam_settings:
                await ctx.send(
                    "❌ การตั้งค่าไม่ถูกต้อง\n"
                    "การตั้งค่าที่มี:\n"
                    "- message_limit: จำนวนข้อความสูงสุดที่อนุญาต\n"
                    "- time_window: ระยะเวลา (วินาที)\n"
                    "- mute_duration: ระยะเวลาลงโทษ (วินาที)\n"
                    "- warning_limit: จำนวนครั้งสูงสุดที่เตือนก่อนเตะ\n"
                    "- warning_reset: ระยะเวลารีเซ็ตการเตือน (วินาที)"
                )
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

    @spam.command(name="status")
    @commands.has_permissions(administrator=True)
    async def spam_status(self, ctx):
        """แสดงสถานะการตั้งค่าระบบป้องกันสแปม"""
        try:
            embed = discord.Embed(
                title="⚙️ สถานะระบบป้องกันสแปม",
                color=discord.Color.blue()
            )
            for setting, value in self.spam_settings.items():
                embed.add_field(
                    name=setting,
                    value=str(value),
                    inline=True
                )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการแสดงสถานะ")
            self.logger.error(f"Error in spam status: {e}")

    @spam.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def spam_reset(self, ctx):
        """รีเซ็ตประวัติการเตือนทั้งหมด"""
        try:
            self.warning_history.clear()
            await ctx.send("✅ รีเซ็ตประวัติการเตือนเรียบร้อยแล้ว")
            self.logger.info("Warning history has been manually reset")
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการรีเซ็ต")
            self.logger.error(f"Error in spam reset: {e}")

    @spam.command(name="patterns")
    @commands.has_permissions(administrator=True)
    async def spam_patterns(self, ctx):
        """แสดงรูปแบบข้อความสแปมทั้งหมด"""
        try:
            embed = discord.Embed(
                title="🔍 รูปแบบข้อความสแปม",
                description="รายการรูปแบบข้อความที่ถูกตรวจจับเป็นสแปม",
                color=discord.Color.blue()
            )
            for i, pattern in enumerate(self.spam_patterns, 1):
                embed.add_field(
                    name=f"รูปแบบที่ {i}",
                    value=f"`{pattern}`",
                    inline=False
                )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการแสดงรูปแบบ")
            self.logger.error(f"Error in spam patterns: {e}")

    @spam.command(name="add")
    @commands.has_permissions(administrator=True)
    async def spam_add_pattern(self, ctx, pattern: str):
        """เพิ่มรูปแบบข้อความสแปม"""
        try:
            if pattern in self.spam_patterns:
                await ctx.send("❌ รูปแบบนี้มีอยู่แล้ว")
                return

            self.spam_patterns.append(pattern)
            await ctx.send(f"✅ เพิ่มรูปแบบ `{pattern}` เรียบร้อยแล้ว")
            self.logger.info(f"Added spam pattern: {pattern}")
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการเพิ่มรูปแบบ")
            self.logger.error(f"Error in spam add pattern: {e}")

    @spam.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def spam_remove_pattern(self, ctx, pattern: str):
        """ลบรูปแบบข้อความสแปม"""
        try:
            if pattern not in self.spam_patterns:
                await ctx.send("❌ ไม่พบรูปแบบนี้")
                return

            self.spam_patterns.remove(pattern)
            await ctx.send(f"✅ ลบรูปแบบ `{pattern}` เรียบร้อยแล้ว")
            self.logger.info(f"Removed spam pattern: {pattern}")
        except Exception as e:
            await ctx.send("❌ เกิดข้อผิดพลาดในการลบรูปแบบ")
            self.logger.error(f"Error in spam remove pattern: {e}")

async def setup(bot):
    await bot.add_cog(SpamProtection(bot))
    logging.info("Spam Protection cog loaded successfully") 