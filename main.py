import discord
from discord.ext import commands
import os
import asyncio
import logging
import sys
from dotenv import load_dotenv
import config
import traceback

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set console encoding to UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    logger.error("No token found in .env file")
    raise ValueError("No token found in .env file")

# Bot setup with intents
intents = discord.Intents.all()

class ManaBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            owner_id=config.OWNER_ID
        )
        self.logger = logger
        self.initial_extensions = [
            'cogs.help',  # Moved help cog to first position
            'cogs.spam_protection',  # Moved spam protection to second position
            'cogs.utility',
            'cogs.moderation',
            'cogs.fun',
            'cogs.filter',
            'cogs.general',
            'cogs.auto_role',
            'cogs.ticket',
            'cogs.welcome'
        ]

    async def setup_hook(self):
        """ตั้งค่าคำสั่งเมื่อบอทเริ่มทำงาน"""
        try:
            # โหลด cogs ทั้งหมด
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    self.logger.info(f"โหลด cog: {filename}")

            # ซิงค์คำสั่งกับเซิร์ฟเวอร์
            guild = discord.Object(id=927993696459304970)  # ID เซิร์ฟเวอร์ของคุณ
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            
            # แสดงคำสั่งที่ลงทะเบียนแล้ว
            commands = await self.tree.fetch_commands(guild=guild)
            for cmd in commands:
                self.logger.info(f"Available command: /{cmd.name} - {cmd.description}")
            
            self.logger.info("ซิงค์คำสั่งเสร็จสิ้น")
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการตั้งค่า: {e}")

    async def on_ready(self):
        """เมื่อบอทพร้อมทำงาน"""
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")
        self.logger.info("------")
        
        # Log all available commands
        try:
            for command in self.tree.get_commands():
                self.logger.info(f'Available command: /{command.name} - {command.description}')
        except Exception as e:
            self.logger.error(f'Error logging commands: {e}')

    async def on_command_error(self, ctx, error):
        """จัดการข้อผิดพลาดของคำสั่ง"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ คำสั่งไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
        else:
            self.logger.error(f'Command error: {error}')
            await ctx.send("❌ เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง")

# Create bot instance
bot = ManaBot()

# Run the bot
if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        asyncio.run(bot.start(TOKEN))
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        traceback.print_exc()