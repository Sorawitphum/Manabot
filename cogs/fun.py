import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp
import json
import datetime

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="diceroll", description="สุ่มตัวเลขระหว่าง 1 ถึงจำนวนที่ระบุ")
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
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="pick", description="สุ่มเลือกจากตัวเลือกที่ให้มา")
    async def choose(self, ctx, *, choices: str):
        """คำสั่งสุ่มเลือกจากตัวเลือกที่ให้มา"""
        choices_list = [choice.strip() for choice in choices.split(',')]
        if len(choices_list) < 2:
            await ctx.send("❌ กรุณาระบุตัวเลือกอย่างน้อย 2 ตัวเลือก (คั่นด้วยเครื่องหมาย ,)")
            return
            
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="🤔 สุ่มเลือก",
            description=f"ตัวเลือกทั้งหมด: {', '.join(choices_list)}\n\nผลลัพธ์: **{choice}**",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="flip", description="โยนเหรียญ")
    async def coinflip(self, ctx):
        """คำสั่งโยนเหรียญ"""
        result = random.choice(["หัว", "ก้อย"])
        embed = discord.Embed(
            title="🪙 โยนเหรียญ",
            description=f"ผลลัพธ์: **{result}**",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="ask", description="ถามคำถามกับ 8ball")
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
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="dice", description="ทอยเต๋า")
    async def dice(self, ctx, amount: int = 1):
        """คำสั่งทอยเต๋า"""
        if amount < 1 or amount > 5:
            await ctx.send("❌ กรุณาระบุจำนวนเต๋าระหว่าง 1-5 ลูก")
            return

        results = [random.randint(1, 6) for _ in range(amount)]
        total = sum(results)
        
        embed = discord.Embed(
            title="🎲 ทอยเต๋า",
            description=f"ผลลัพธ์: {', '.join(map(str, results))}\nผลรวม: **{total}**",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="rps", description="เล่นเป่ายิ้งฉุบ")
    async def rps(self, ctx, choice: str):
        """คำสั่งเล่นเป่ายิ้งฉุบ"""
        choices = ["ค้อน", "กระดาษ", "กรรไกร"]
        if choice.lower() not in ["ค้อน", "กระดาษ", "กรรไกร"]:
            await ctx.send("❌ กรุณาเลือก: ค้อน, กระดาษ, หรือ กรรไกร")
            return

        bot_choice = random.choice(choices)
        
        # ตรวจสอบผู้ชนะ
        if choice == bot_choice:
            result = "เสมอ!"
        elif (choice == "ค้อน" and bot_choice == "กรรไกร") or \
             (choice == "กระดาษ" and bot_choice == "ค้อน") or \
             (choice == "กรรไกร" and bot_choice == "กระดาษ"):
            result = "คุณชนะ! 🎉"
        else:
            result = "คุณแพ้! 😢"

        embed = discord.Embed(
            title="✂️ เป่ายิ้งฉุบ",
            description=f"คุณเลือก: **{choice}**\nบอทเลือก: **{bot_choice}**\n\n{result}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="random", description="สุ่มตัวเลขระหว่างค่าที่ระบุ")
    async def random_range(self, ctx, min_num: int, max_num: int):
        """คำสั่งสุ่มตัวเลขระหว่างค่าที่ระบุ"""
        if min_num >= max_num:
            await ctx.send("❌ ค่าตัวเลขแรกต้องน้อยกว่าค่าตัวเลขที่สอง")
            return

        number = random.randint(min_num, max_num)
        embed = discord.Embed(
            title="🎲 สุ่มตัวเลข",
            description=f"ระหว่าง {min_num} ถึง {max_num}\n\nผลลัพธ์: **{number}**",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"คำขอโดย {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot)) 