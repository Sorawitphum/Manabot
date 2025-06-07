"""
config for ManaBot TH
รวมการตั้งค่าทั้งหมดของบอท ข้อความ และตัวเลือกที่สามารถปรับแต่งได้

ไฟล์นี้ประกอบด้วยการตั้งค่าต่าง ๆ สำหรับบอท เช่น:
- การตั้งค่าพื้นฐานของบอท (prefix, color, emoji)
- หมวดหมู่คำสั่งและคำอธิบาย
- ข้อความแจ้งเตือนข้อผิดพลาดและความสำเร็จ
- ข้อความต้อนรับสมาชิกใหม่
- การตั้งค่าแจกบทบาทอัตโนมัติ
- การตั้งค่าระบบกรองคำ
- การตั้งค่าระบบ Ticket
- การตั้งค่าระบบโหวต
- การตั้งค่า fun command
"""
# Bot Configuration
TOKEN = "YOUR_BOT_TOKEN"
OWNER_ID = 843692169000648706  # ใส่ ID ของเจ้าของบอทตรงนี้

# Support Server Configuration
SUPPORT_SERVER_LINK = "https://discord.gg/ArXRg7E4"  # ใส่ลิงก์เชิญเซิร์ฟเวอร์สนับสนุนตรงนี้

# Bot Settings
BOT_PREFIX = "!"  # Command prefix
BOT_COLOR = 0x2B2D31  # Default embed color
BOT_EMOJI = "✨"  # Default emoji

# Bot Owner


# Command Categories
COMMAND_CATEGORIES = {
    "🏠 คำสั่งทั่วไป": {
        "ping": "ตรวจสอบการตอบสนองของบอท",
        "invite": "รับลิงก์เชิญบอท",
        "support": "รับลิงก์เซิร์ฟเวอร์สนับสนุน",
        "vote": "โหวตให้บอท",
        "donate": "สนับสนุนผู้พัฒนา"
    },
    "📢 ระบบประกาศ": {
        "announce": "ส่งประกาศไปยังช่องที่เลือก (ต้องมีบทบาท admin/staff)",
        "announcement": "ดูคำสั่งประกาศทั้งหมด"
    },
    "🎮 คำสั่งสนุก": {
        "diceroll": "สุ่มตัวเลข 1 ถึงจำนวนที่ระบุ",
        "pick": "สุ่มเลือกจากตัวเลือกที่ให้มา",
        "flip": "โยนเหรียญ",
        "ask": "ถามคำถามกับ 8ball",
        "dice": "ทอยเต๋า 1-5 ลูก",
        "rps": "เล่นเป่ายิ้งฉุบ",
        "random": "สุ่มตัวเลขระหว่างค่าที่กำหนด",
        "roll": "สุ่มตัวเลข 1 ถึงจำนวนที่ระบุ",
        "choose": "สุ่มเลือกจากตัวเลือกที่ให้มา",
        "coinflip": "โยนเหรียญ",
        "8ball": "ถามคำถามกับ 8ball"
    },
    "ℹ️ คำสั่งข้อมูล": {
        "userinfo": "ดูข้อมูลผู้ใช้",
        "serverinfo": "ดูข้อมูลเซิร์ฟเวอร์",
        "roleinfo": "ดูข้อมูลบทบาท",
        "avatar": "ดูรูปโปรไฟล์ผู้ใช้",
        "user": "ดูข้อมูลผู้ใช้"
    },
    "🛡️ คำสั่งจัดการ": {
        "kick": "เตะผู้ใช้ช้ออกจากเซิร์ฟเวอร์",
        "ban": "แบนผู้ใช้จากเซิร์ฟเวอร์",
        "clear": "ลบข้อความ",
        "timeout": "ระงับผู้ใช้ชั่วคราว"
    },
    "🎫 ระบบ Ticket": {
        "ticket": "สร้าง ticket สำหรับติดต่อทีมงาน"
    },
    "👥 ระบบ Auto Role": {
        "autorole": "ตั้งค่าบทบาทอัตโนมัติสำหรับสมาชิกใหม่"
    },
    "🔧 คำสั่งอื่นๆ": {
        "poll": "สร้างโพลแบบง่าย"
    }
}

# Error Messages
ERROR_MESSAGES = {
    "command_not_found": "❌ คำสั่งไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง",
    "missing_permissions": "❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้",
    "missing_arguments": "❌ กรุณาระบุข้อมูลให้ครบถ้วน",
    "member_not_found": "❌ ไม่พบผู้ใช้นี้",
    "role_hierarchy": "❌ คุณไม่สามารถจัดการผู้ใช้ที่มีบทบาทสูงกว่าหรือเท่ากับคุณได้",
    "bot_permission": "❌ ขออภัย ฉันไม่มีสิทธิ์ดำเนินการนี้",
    "invalid_amount": "❌ กรุณาระบุจำนวนที่ถูกต้อง",
    "invalid_time": "❌ กรุณาระบุเวลาระหว่าง 1-40320 นาที",
    "invalid_role": "❌ ไม่พบบทบาทที่ระบุ",
    "invalid_channel": "❌ ไม่พบช่องที่ระบุ",
    "invalid_category": "❌ ไม่พบหมวดหมู่ที่ระบุ"
}

# Success Messages
SUCCESS_MESSAGES = {
    "kick": "👢 เตะผู้ใช้สำเร็จ",
    "ban": "🔨 แบนผู้ใช้สำเร็จ",
    "clear": "🧹 ลบข้อความสำเร็จ",
    "timeout": "⏰ ระงับผู้ใช้สำเร็จ",
    "ticket_created": "🎫 สร้าง ticket สำเร็จ",
    "ticket_closed": "🔒 ปิด ticket สำเร็จ",
    "role_added": "✅ เพิ่มบทบาทสำเร็จ",
    "role_removed": "✅ ลบบทบาทสำเร็จ",
    "poll_created": "📊 สร้างโพลสำเร็จ"
}

# Welcome Messages
WELCOME_MESSAGES = [
    "ยินดีต้อนรับ {member} เข้าสู่ {server}! 🎉",
    "สวัสดี {member} ยินดีต้อนรับสู่ {server}! 🌟",
    "เฮ้ {member}! ยินดีต้อนรับสู่ {server}! 🎊",
    "ยินดีต้อนรับ {member} เข้ามาเป็นส่วนหนึ่งของ {server}! 🎈"
]

# Auto Role Settings
AUTO_ROLE = {
    "enabled": True,
    "roles": []  # Add role IDs here
}

# Filter Settings
FILTER = {
    "enabled": True,
    "banned_words": [],  # Add banned words here
    "ignored_channels": [],  # Add channel IDs to ignore
    "ignored_roles": []  # Add role IDs to ignore
}

# Ticket Settings
TICKET = {
    "enabled": True,
    "category_id": None,  # Add category ID for tickets
    "support_role_id": None,  # Add support role ID
    "log_channel_id": None  # Add log channel ID
}

# Poll Settings
POLL = {
    "max_options": 10,
    "max_duration": 604800,  # 7 days in seconds
    "default_duration": 86400  # 24 hours in seconds
}

# Fun Command Settings
FUN = {
    "8ball_responses": [
        "ใช่ แน่นอน! ✨",
        "ไม่ ไม่มีทาง! ❌",
        "อาจจะเป็นไปได้ 🤔",
        "ลองถามใหม่สิ 🔄",
        "แน่นอนที่สุด! 🌟",
        "ไม่แน่ใจนะ 🤷‍♂️",
        "ใช่! 🎯",
        "ไม่! 🚫",
        "ลองดูสิ 👀",
        "ไม่น่าจะเป็นไปได้ 😕"
    ],
    "rps_options": ["ค้อน", "กระดาษ", "กรรไกร"],
    "dice_max": 5,
    "random_max": 1000000
}

# Feedback System
FEEDBACK_CHANNEL_ID = 1380910647583309975 # ID ของช่องสำหรับรับ feedback
ANNOUNCEMENT_LOG_CHANNEL_ID = None  # ใส่ ID ของช่อง log การประกาศ

# Spam Protection Settings
SPAM_PROTECTION = {
    'message_limit': 5,     # จำนวนข้อความสูงสุดที่อนุญาต
    'time_window': 5,       # ระยะเวลา (วินาที)
    'mute_duration': 300,   # ระยะเวลาลงโทษ (วินาที)
    'patterns': [           # รูปแบบข้อความสแปม
        r'(?i)(?:http|https)://',
        r'(?i)(?:discord\.gg|discord\.com/invite)',
        r'(?i)(?:@everyone|@here)',
        r'(?i)(?:free|nitro|gift)',
    ]
}

# Announcement System Settings
ANNOUNCEMENT_ROLES = ["admin", "staff", "Administrator"]  # บทบาทที่สามารถใช้คำสั่งประกาศได้
ANNOUNCEMENT_TEMPLATES = {
    "normal": {
        "title": "📢 ประกาศ",
        "color": "#3498db",  # สีฟ้า
        "icon": "announce.svg"  # ไอคอนประกาศ
    },
    "warning": {
        "title": "⚠️ แจ้งเตือน",
        "color": "#e74c3c",  # สีแดง
        "icon": "warning.svg"  # ไอคอนเตือน
    },
    "event": {
        "title": "🎉 กิจกรรม",
        "color": "#2ecc71",  # สีเขียว
        "icon": "event.svg"  # ไอคอนกิจกรรม
    }
} 