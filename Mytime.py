import asyncio
import random
import time

from telethon.tl.functions.account import UpdateProfileRequest

from .. import JmdB, jmubot, jmthon_cmd

USERBIO = JmdB.get_key("MYBIO") or "صلى الله على محمد و أهل بيته"
NAME = JmdB.get_key("NAME") or "User"

BIOS = [
    "الحمد لله رب العالمين",
    "صلى الله على محمد و أهل بيته",
    "أستغفر الله العلي العظيم",
]

@jmthon_cmd(pattern="اسم وقتي$")
async def autoname(event):
    if JmdB.get_key("AUTONAME"):
        return await event.eor("**⌔∮ الاسم الوقتي يعمل بالفعل**")
    
    JmdB.set_key("AUTONAME", "True")
    await event.eor("**⌔∮ تم تفعيل الاسم الوقتي**")
    
    while JmdB.get_key("AUTONAME"):
        try:
            current_time = time.strftime("%I:%M")
            await event.client(UpdateProfileRequest(first_name=current_time))
            await asyncio.sleep(60)
        except Exception as e:
            print(f"[AutoName Error] {e}")
            await asyncio.sleep(60)

@jmthon_cmd(pattern="بايو وقتي$")
async def autobio(event):
    if JmdB.get_key("AUTOBIO"):
        return await event.eor("**⌔∮ البايو الوقتي يعمل بالفعل**")
    
    JmdB.set_key("AUTOBIO", "True")
    await event.eor("**⌔∮ تم تفعيل البايو الوقتي**")
    
    while JmdB.get_key("AUTOBIO"):
        try:
            current_time = time.strftime("%I:%M")
            bio_text = JmdB.get_key("MYBIO") or random.choice(BIOS)
            full_bio = f"{bio_text} | {current_time}"
            await event.client(UpdateProfileRequest(about=full_bio))
            await asyncio.sleep(60)
        except Exception as e:
            print(f"[AutoBio Error] {e}")
            await asyncio.sleep(60)

@jmthon_cmd(pattern=r"انهاء (.+)")
async def stop_auto(event):
    input_str = event.pattern_match.group(1).strip()
    
    if input_str in ["اسم وقتي", "اسم الوقتي", "الاسم الوقتي", "الاسم وقتي"]:
        if JmdB.get_key("AUTONAME"):
            JmdB.del_key("AUTONAME")
            await event.client(UpdateProfileRequest(first_name=NAME))
            return await event.eor("**⌔∮ تم إيقاف الاسم الوقتي بنجاح**")
        return await event.eor("**⌔∮ الاسم الوقتي غير مفعّل**")
    
    elif input_str in ["بايو وقتي", "البايو الوقتي"]:
        if JmdB.get_key("AUTOBIO"):
            JmdB.del_key("AUTOBIO")
            await event.client(UpdateProfileRequest(about=USERBIO))
            return await event.eor("**⌔∮ تم إيقاف البايو الوقتي بنجاح**")
        return await event.eor("**⌔∮ البايو الوقتي غير مفعّل**")
    
    else:
        return await event.eor("**⌔∮ الأمر غير معروف، تأكد من الصياغة**")

@jmthon_cmd(pattern="حالة وقتية$")
async def time_status(event):
    name_status = "✅" if JmdB.get_key("AUTONAME") else "❌"
    bio_status = "✅" if JmdB.get_key("AUTOBIO") else "❌"
    
    msg = f"""**⌔∮ حالة التفعيل الحالية:**

• الاسم الوقتي: {name_status}
• البايو الوقتي: {bio_status}"""
    
    await event.eor(msg)
