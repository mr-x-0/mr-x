from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch 
import os
import aiohttp
import requests
import random 
import asyncio
import yt_dlp
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import pytgcalls
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
from typing import Union
from pyrogram import Client, filters 
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError,AlreadyJoinedError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
import asyncio
from config import *
import numpy as np
from yt_dlp import YoutubeDL
from config import user, dev, call, logger, logger_mode, botname, appp
from CASERr.daty import get_call, get_userbot, get_dev, get_logger, del_userbot, del_call
from pyrogram import Client
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from CASERr.CASERr import get_channel, devchannel, source, caes, devgroup, devuser, group, casery, johned, photosource
from io import BytesIO
import aiofiles
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def gen_bot_caesar(client, bot_username, OWNER_ID, CASER, message, videoid):
    if os.path.isfile(f"photos/{videoid}_{bot_username}.png"):
        return f"photos/{videoid}_{bot_username}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(10))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("font.ttf", 70)
        caesa = ImageFont.truetype("font.ttf", 45)        
        box_size = (500, 500)
        box_position = (40, 100)
        box_image = Image.new("RGBA", box_size, (255, 255, 255, 0))
        box_draw = ImageDraw.Draw(box_image)
        box_draw.ellipse([(0, 0), box_size], outline="white", width=5)               
        wxyz = await client.get_chat(OWNER_ID)
        CAR = wxyz.username
        vvv = wxyz.photo.big_file_id
        wxy = await client.download_media(vvv)
        inner_image = Image.open(wxy)
        inner_image = inner_image.resize((480, 480))
        box_image.paste(inner_image, (10, 10))  
        background.paste(box_image, box_position)   
        draw.text((600, 120), "MuSiC AlQaId", fill="white", stroke_width=2, stroke_fill="white", font=arial)     
        draw.text((600, 420), f"{channel} | {views[:23]}", (255, 255, 255), font=caesa)        
        draw.text((600, 490), f"Channel : {channel}", (255, 255, 255), font=caesa)       
        draw.text((600, 350), f"Views : {views[:23]}", (255, 255, 255), font=caesa) 
        draw.text((600, 550), f"Duration : {duration[:23]} Mins", (255, 255, 255), font=caesa)    
        background.save(f"photos/{videoid}_{bot_username}.png")
        os.remove(f"thumb{videoid}.png")
        file = f"photos/{videoid}_{bot_username}.png"
        return file
    except Exception as e:
        print(e)
        
playlist = {}
vidd = {}
namecha = {}
user_mentio = {}
thu = {}
phot = {}
        
async def join_call(bot_username, OWNER_ID, client, message, audio_file, group_id, vid, user_mention, photo, thum, namechat): 
    userbot = await get_userbot(bot_username)
    hoss = await get_call(bot_username)    
    devus = devuser.get(bot_username) if devuser.get(bot_username) else f"{casery}"
    soesh = devchannel.get(bot_username) if devchannel.get(bot_username) else f"{source}"
    gr = devgroup.get(bot_username) if devgroup.get(bot_username) else f"{group}"
    usr = await client.get_chat(devus)
    user_id = usr.id
    CASER = usr.username
    name = usr.first_name
    Done = None
    file_path = audio_file
    audio_stream_quality = MediumQualityAudio()
    video_stream_quality = MediumQualityVideo()
    stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))
    try:
        await hoss.join_group_call(message.chat.id, stream, stream_type=StreamType().pulse_stream)
        Done = True
    except NoActiveGroupCall:
        buttoon = [[InlineKeyboardButton(text="تحديث ♻️", callback_data=f"reboott")]]
        await client.send_message(message.chat.id, "**حدث خطا اثناء التشغيل\nاضغط علي الزر بالاسفل لتحديث ♻️\nاو تاكد من تشغيل المكالمه الصوتيه**", reply_markup=InlineKeyboardMarkup(buttoon))
    except AlreadyJoinedError:
        if group_id not in playlist:
         playlist[group_id] = [] 
         vidd[group_id] = [] 
         namecha[group_id] = [] 
         user_mentio[group_id] = [] 
         thu[group_id] = [] 
         phot[group_id] = [] 
        if group_id not in playlist[group_id]:
         playlist[group_id].append(file_path)
         vidd[group_id].append(vid)
         namecha[group_id].append(namechat)
         user_mentio[group_id].append(user_mention)
         thu[group_id].append(thum)
         phot[group_id].append(photo)
        if group_id in playlist:
         count = len(playlist[group_id])
        loggerlink = await client.export_chat_invite_link(group_id)
        button = [[InlineKeyboardButton(text="𝗘𝗻𝗗", callback_data=f"stop"), InlineKeyboardButton(text="𝗥𝗲𝗦𝘂𝗠𝗲", callback_data=f"resume"), InlineKeyboardButton(text="𝗣𝗲𝗨𝘀𝗘", callback_data=f"pause")], [InlineKeyboardButton(text="𝗖𝗵𝗔𝗻𝗘𝗲𝗟", url=f"{soesh}"), InlineKeyboardButton(text="𝗚𝗿𝗢𝘂𝗣", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
        await client.send_photo(group_id, photo=photo, caption=f"**𝗔𝗱𝗗 𝗦𝗼𝗡𝗴 𝗧𝗼 𝗣𝗹𝗔𝘆 : {count}\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id)
    except TelegramServerError:
        await client.send_message(message.chat.id, "**حدث خطأ في الخادم...**")
    except Exception as e:
        print(e)
    
    return Done

async def Call(bot_username):
    hoss = await get_call(bot_username)
    @hoss.on_stream_end()
    async def stream_end_handler1(client, update: Update):
        if not isinstance(update, StreamAudioEnded):
            return        
        await change_stream(bot_username, update.chat_id, client)

async def change_stream(bot_username, chat_id, client): 
    hoss = await get_call(bot_username)    
    OWNER_ID = await get_dev(bot_username)
    logger = await get_logger(bot_username)
    devus = devuser.get(bot_username) if devuser.get(bot_username) else f"{casery}"
    soesh = devchannel.get(bot_username) if devchannel.get(bot_username) else f"{source}"
    gr = devgroup.get(bot_username) if devgroup.get(bot_username) else f"{group}"
    apppp = appp[bot_username]
    usr = await apppp.get_chat(devus)
    user_id = usr.id
    CASER = usr.username
    name = usr.first_name
    if chat_id in playlist and playlist[chat_id] and vidd and vidd[chat_id] and namecha and namecha[chat_id] and user_mentio and user_mentio[chat_id] and thu and thu[chat_id] and phot and phot[chat_id]:
        next_song = playlist[chat_id].pop(0)
        vid = vidd[chat_id].pop(0)
        namechat = namecha[chat_id].pop(0)
        user_mention = user_mentio[chat_id].pop(0)       
        thum = thu[chat_id].pop(0)        
        photo = phot[chat_id].pop(0)
        file_path = next_song       
        photo = photo
        user_mention = user_mention
        thum = thum
        namechat = namechat        
        try:
            audio_stream_quality = MediumQualityAudio()
            video_stream_quality = MediumQualityVideo()
            stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))
            await hoss.change_stream(chat_id, stream)
            loggerlink = await apppp.export_chat_invite_link(chat_id)
            button = [[InlineKeyboardButton(text="𝗘𝗻𝗗", callback_data=f"stop"), InlineKeyboardButton(text="𝗥𝗲𝗦𝘂𝗠𝗲", callback_data=f"resume"), InlineKeyboardButton(text="𝗣𝗲𝗨𝘀𝗘", callback_data=f"pause")], [InlineKeyboardButton(text="𝗖𝗵𝗔𝗻𝗘𝗲𝗟", url=f"{soesh}"), InlineKeyboardButton(text="𝗚𝗿𝗢𝘂𝗣", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
            await apppp.send_photo(chat_id, photo=photo, caption=f"**𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button))
            await apppp.send_message(logger, f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁ |𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n⌁ |𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n⌁ |𝗕𝘆 : {user_mention}\n⌁ |𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})\n\n╰── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╯**", disable_web_page_preview=True)
        except Exception as e:
            pass
    else:
        try:
            await hoss.leave_group_call(chat_id)
        except Exception as e:
            print("يعم فوق مفيش حاجه شغاله 😹🎶لا")

async def download(bot_username, link, video: Union[bool, str] = None):
    link = link
    loop = asyncio.get_running_loop()
    def audio_dl():
        ydl_opts = {"format": "bestaudio/best", "outtmpl": f"Music/{bot_username}/%(id)s.%(ext)s", "geo_bypass": True, "nocheckcertificate": True, "quiet": True, "no_warnings": True, "username": "oauth2", "password" : ""}
        x = yt_dlp.YoutubeDL(ydl_opts)
        info = x.extract_info(link, False)
        xyz = os.path.join(f"Music/{bot_username}/{info['id']}.{info['ext']}")
        if os.path.exists(xyz):
            return xyz
        x.download([link])
        return xyz
    if video:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--username", "oauth2",
            "--password", "",
            "-g",
            "-f", "bestvideo[height<=?720][width<=?1280]+bestaudio/best",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            downloaded_file = stdout.decode().split("\n")[0]
        else:
            return
    else:
        downloaded_file = await loop.run_in_executor(None, audio_dl)
    return downloaded_file
 
@Client.on_message(filters.command(["انضم"], ""), group=575580)
async def mson5454hfbg(client, message):
        hoss_chat_user = message.chat.id
        bot_username = client.me.username
        user = await get_userbot(bot_username) 
        hos_info = await client.get_chat(hoss_chat_user)    
        if hos_info.invite_link:
          hos_link = hos_info.invite_link
        else:
          await message.reply("لا يمكن العثور على رابط الدعوة لهذه المجموعة/القناة\n قم برفعي مشرف في الجروب أولاً")
          return
        try:
          await user.join_chat(str(hos_link))
        except Exception as e:
          print(f"حدث خطأ أثناء الانضمام: {str(e)}")

@Client.on_message(filters.command(["/reboot"], ""), group=57557580)
async def mson5674hfbg(client, message):
        hoss_chat_user = message.chat.id
        bot_username = client.me.username
        h = await message.reply_text("جاري التحديث انتظر ♻️")
        await asyncio.sleep(5)
        try: 
          user = await del_userbot(bot_username) 
          call = await del_call(bot_username) 
          await Call(bot_username)
          await h.edit_text("تم التحديث بنجاح ♻️✅")
        except Exception as e:
          await message.reply_text("حدث خطا اثناء التحديث")
          
@Client.on_callback_query(filters.regex(pattern=r"^(reboott)$"))
async def rebootthd(client: Client, CallbackQuery):
    bot_username = client.me.username 
    hoss = await get_call(bot_username)
    a = await client.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     return await CallbackQuery.answer("يجب انت تكون ادمن للقيام بذلك  !", show_alert=True)
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id
    await CallbackQuery.message.delete()
    if command == "reboott":
        try:
         h = await CallbackQuery.message.reply_text("**جاري التحديث انتظر ♻️**")
         await asyncio.sleep(5)
         user = await del_userbot(bot_username) 
         call = await del_call(bot_username) 
         await Call(bot_username)
         await h.edit_text("**تم التحديث بنجاح ♻️✅**")
        except Exception as e:
         await CallbackQuery.message.reply_text(f"**حدث خطا اثناء التحديث**")
                  
@Client.on_message(filters.text & filters.group) 
async def leave_group(client, message):
   bot_username = client.me.username
   OWNER_ID = await get_dev(bot_username)
   if message.from_user.id == OWNER_ID or message.from_user.username in caes:
     if message.text == "اخرج": 
        await message.reply_text("سأغادر الآن 👋")
        await client.leave_chat(message.chat.id)

Music = {}

@Client.on_message(filters.command(["قفل الميوزك"], ""),group=18798)
async def abra245g(client, message):
   bot_username = client.me.username
   OWNER_ID = await get_dev(bot_username)
   if message.from_user.id == OWNER_ID or message.from_user.username in caes:
    Music.setdefault(bot_username, []).append(bot_username)
    await message.reply_text(f"• تم قفل الميوزك بواسطه ↤︎「 {message.from_user.mention}")

@Client.on_message(filters.command(["فتح الميوزك"], ""),group=545177)
async def abr54ag(client, message):
   bot_username = client.me.username
   OWNER_ID = await get_dev(bot_username)
   if message.from_user.id == OWNER_ID or message.from_user.username in caes:
    Music[bot_username].remove(bot_username)
    await message.reply_text(f"• تم فتح الميوزك بواسطه ↤︎「 {message.from_user.mention}")

yoro = ["Xnxx", "سكس","اباحيه","جنس","اباحي","زب","كسمك","كس","شرمطه","نيك","لبوه","فشخ","مهبل","نيك خلفى","بتتناك","مساج","كس ملبن","نيك جماعى","نيك جماعي","نيك بنات","رقص","قلع","خلع ملابس","بنات من غير هدوم","بنات ملط","نيك طيز","نيك من ورا","نيك في الكس","ارهاب","موت","حرب","سياسه","سياسي","سكسي","قحبه","شواز","ممويز","نياكه","xnxx","sex","xxx","Sex","Born","borno","Sesso"]

@Client.on_message(filters.command(["شغل", "تشغيل", "فيد", "فديو", "/vplay", "/play"], "") & filters.group, group=57655580)
async def msonhfbg(client, message):
    if await johned(client, message):
     return
    bot_username = client.me.username
    user = await get_userbot(bot_username) 
    hoss = await get_call(bot_username)
    devus = devuser.get(bot_username) if devuser.get(bot_username) else f"{casery}"
    soesh = devchannel.get(bot_username) if devchannel.get(bot_username) else f"{source}"
    gr = devgroup.get(bot_username) if devgroup.get(bot_username) else f"{group}"
    OWNER_ID = await get_dev(bot_username)
    logger = await get_logger(bot_username)
    usr = await client.get_chat(devus)
    CASER = usr.username
    name = usr.first_name
    group_id = message.chat.id
    if message.reply_to_message:
     if "v" in message.command[0] or "ف" in message.command[0]:
      vid = True
     else:
      vid = None
     mhm = await message.reply_text("**جاري تحميل الريك او الفديو انتظر**")
     photo = photosource
     audio_file = await message.reply_to_message.download()
     thum = None
     namechat = f"{message.chat.title}"
     button = [[InlineKeyboardButton(text="𝐄𝐍𝐃", callback_data=f"stop"), InlineKeyboardButton(text="𝐑𝐄𝐒𝐔𝐌𝐄", callback_data=f"resume"), InlineKeyboardButton(text="𝐏𝐄𝐔𝐒𝐄", callback_data=f"pause")], [InlineKeyboardButton(text="𝐂𝐇𝐀𝐍𝐄𝐋", url=f"{soesh}"), InlineKeyboardButton(text="𝐆𝐑𝐎𝐔𝐏", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
     loggerlink = message.chat.username if message.chat.username else message.chat.title
     if message.from_user is not None:
      user_mention = f"{message.from_user.mention}"
     else: 
      user_mention = f"{message.author_signature}"
     c = await join_call(bot_username, OWNER_ID, client, message, audio_file, group_id, vid, user_mention, photo, thum, namechat)
     await mhm.delete()
     os.remove(audio_file)
     if not c:
         return
     await client.send_photo(group_id, photo=photo, caption=f"**𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id)
     await client.send_message(logger, f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁ |𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n⌁ |𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n⌁ |𝗕𝘆 : {user_mention}\n⌁ |𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})\n\n╰── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╯**", disable_web_page_preview=True)
    elif message.text:
     try:
      text = message.text.split(None, 1)[1]
     except Exception as e:
      nme = await client.ask(message.chat.id, text="**القمر عيز يشغل اي 😂♥🎵**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=200)
      text = nme.text
    else:
        return
    if text in yoro:
      return await message.reply_text("**مش بشغل حاجه حرام 🙄😹**")  
    else:      
     print("احم")    
    mm = await message.reply_text("**جاري التشغيل يقلبي ✨♥🎵**")    
    try:
     results = VideosSearch(text, limit=1)
    except Exception:
      return 
    for result in (await results.next())["result"]:
      thum = result["title"]
      duration = result["duration"]
      videoid = result["id"]
      yturl = result["link"]
      thumbnail = result["thumbnails"][0]["url"].split("?")[0]
    if "v" in message.command[0] or "ف" in message.command[0]:
      vid = True
    else:
      vid = None
    results = YoutubeSearch(text, max_results=5).to_dict()
    link = f"https://youtube.com{results[0]['url_suffix']}"
    audio_file = await download(bot_username, link, vid)
    photo = await gen_bot_caesar(client, bot_username, OWNER_ID, CASER, message, videoid)   
    namechat = f"{message.chat.title}"     
    button = [[InlineKeyboardButton(text="𝐄𝐍𝐃", callback_data=f"stop"), InlineKeyboardButton(text="𝐑𝐄𝐒𝐔𝐌𝐄", callback_data=f"resume"), InlineKeyboardButton(text="𝐏𝐄𝐔𝐒𝐄", callback_data=f"pause")], [InlineKeyboardButton(text="𝐂𝐇𝐀𝐍𝐄𝐋", url=f"{soesh}"), InlineKeyboardButton(text="𝐆𝐑𝐎𝐔𝐏", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
    loggerlink = await client.export_chat_invite_link(group_id)
    await mm.delete()
    if message.from_user is not None:
      user_mention = f"{message.from_user.mention}"
    else: 
      user_mention = f"{message.author_signature}"
    c = await join_call(bot_username, OWNER_ID, client, message, audio_file, group_id, vid, user_mention, photo, thum, namechat)
    if not c:
         return
    await client.send_photo(group_id, photo=photo, caption=f"**𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id)
    await client.send_message(logger, f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁ |𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n⌁ |𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n⌁ |𝗕𝘆 : {user_mention}\n⌁ |𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})\n\n╰── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╯**", disable_web_page_preview=True)
    try:
         return
    except:
         pass

@Client.on_message(filters.command(["شغل", "تشغيل", "فيد", "فديو", "/vplay", "/play"], "") & filters.channel, group=57655580)
async def msonhfbhdhjhg(client, message):
    bot_username = client.me.username
    user = await get_userbot(bot_username) 
    hoss = await get_call(bot_username)
    devus = devuser.get(bot_username) if devuser.get(bot_username) else f"{casery}"
    soesh = devchannel.get(bot_username) if devchannel.get(bot_username) else f"{source}"
    gr = devgroup.get(bot_username) if devgroup.get(bot_username) else f"{group}"
    OWNER_ID = await get_dev(bot_username)
    logger = await get_logger(bot_username)
    usr = await client.get_chat(devus)
    CASER = usr.username
    name = usr.first_name
    group_id = message.chat.id
    if message.reply_to_message:
     if "v" in message.command[0] or "ف" in message.command[0]:
      vid = True
     else:
      vid = None
     mhm = await message.reply_text("**جاري تحميل الريك او الفديو انتظر**")
     photo = photosource
     audio_file = await message.reply_to_message.download()
     thum = None
     namechat = f"{message.chat.title}"
     button = [[InlineKeyboardButton(text="𝐄𝐍𝐃", callback_data=f"stop"), InlineKeyboardButton(text="𝐑𝐄𝐒𝐔𝐌𝐄", callback_data=f"resume"), InlineKeyboardButton(text="𝐏𝐄𝐔𝐒𝐄", callback_data=f"pause")], [InlineKeyboardButton(text="𝐂𝐇𝐀𝐍𝐄𝐋", url=f"{soesh}"), InlineKeyboardButton(text="𝐆𝐑𝐎𝐔𝐏", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
     loggerlink = message.chat.username if message.chat.username else message.chat.title
     if message.from_user is not None:
      user_mention = f"{message.from_user.mention}"
     else: 
      user_mention = f"{message.author_signature}"
     c = await join_call(bot_username, OWNER_ID, client, message, audio_file, group_id, vid, user_mention, photo, thum, namechat)
     await mhm.delete()
     os.remove(audio_file)
     if not c:
         return
     await client.send_photo(group_id, photo=photo, caption=f"**𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id)
     await client.send_message(logger, f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁ |𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n⌁ |𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n⌁ |𝗕𝘆 : {user_mention}\n⌁ |𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})\n\n╰── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╯**", disable_web_page_preview=True)
    elif message.text:
     try:
      text = message.text.split(None, 1)[1]
     except Exception as e:
      nme = await client.ask(message.chat.id, text="**القمر عيز يشغل اي 😂♥🎵**", reply_to_message_id=message.id, timeout=200)
      text = nme.text
    else:
        return
    if text in yoro:
      return await message.reply_text("**مش بشغل حاجه حرام 🙄😹**")  
    else:      
     print("احم")    
    mm = await message.reply_text("**جاري التشغيل يقلبي ✨♥🎵**")    
    try:
     results = VideosSearch(text, limit=1)
    except Exception:
      return 
    for result in (await results.next())["result"]:
      thum = result["title"]
      duration = result["duration"]
      videoid = result["id"]
      yturl = result["link"]
      thumbnail = result["thumbnails"][0]["url"].split("?")[0]
    if "v" in message.command[0] or "ف" in message.command[0]:
      vid = True
    else:
      vid = None
    results = YoutubeSearch(text, max_results=5).to_dict()
    link = f"https://youtube.com{results[0]['url_suffix']}"
    audio_file = await download(bot_username, link, vid)
    photo = await gen_bot_caesar(client, bot_username, OWNER_ID, CASER, message, videoid)   
    namechat = f"{message.chat.title}"     
    button = [[InlineKeyboardButton(text="𝐄𝐍𝐃", callback_data=f"stop"), InlineKeyboardButton(text="𝐑𝐄𝐒𝐔𝐌𝐄", callback_data=f"resume"), InlineKeyboardButton(text="𝐏𝐄𝐔𝐒𝐄", callback_data=f"pause")], [InlineKeyboardButton(text="𝐂𝐇𝐀𝐍𝐄𝐋", url=f"{soesh}"), InlineKeyboardButton(text="𝐆𝐑𝐎𝐔𝐏", url=f"{gr}")], [InlineKeyboardButton(text=f"{name}", url=f"https://t.me/{CASER}")], [InlineKeyboardButton(text="𝗔𝗱𝗗 𝗕𝗼𝗧 𝗧𝗼 𝗬𝗼𝗨𝗿 𝗚𝗿𝗢𝘂𝗣", url=f"https://t.me/{bot_username}?startgroup=True")]]
    loggerlink = await client.export_chat_invite_link(group_id)
    await mm.delete()
    if message.from_user is not None:
      user_mention = f"{message.from_user.mention}"
    else: 
      user_mention = f"{message.author_signature}"
    c = await join_call(bot_username, OWNER_ID, client, message, audio_file, group_id, vid, user_mention, photo, thum, namechat)
    if not c:
         return
    await client.send_photo(group_id, photo=photo, caption=f"**𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n𝗕𝘆 : {user_mention}\n𝗚??𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})**", reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id)
    await client.send_message(logger, f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁ |𝗣𝗹𝗔𝘆𝗜𝗻𝗚 𝗡𝗼𝗪 𝗦𝘁𝗔𝗿𝗧𝗲𝗗\n\n⌁ |𝗦𝗼𝗡𝗴 𝗡𝗮𝗠𝗲 : `{thum}`\n⌁ |𝗕𝘆 : {user_mention}\n⌁ |𝗚𝗿𝗢𝘂𝗣 𝗕𝘆 : [{namechat}]({loggerlink})\n\n╰── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╯**", disable_web_page_preview=True)
    try:
         return
    except:
         pass

@Client.on_message(filters.command(["تحكم"], ""), group=9736055)
async def gers(client, message):
    bot_username = client.me.username 
    soesh = devchannel.get(bot_username) if devchannel.get(bot_username) else f"{source}"
    global thu
    o = 1
    button = [[InlineKeyboardButton(text="𝗘𝗻𝗗 ⤶", callback_data=f"stop"), InlineKeyboardButton(text="𝗦𝗸𝗶𝗽 ⤶", callback_data=f"skip")]]
    group_id = message.chat.id
    if group_id in thu:
        count = len(thu[group_id])
        user_mentions = [str(user) for user in thu[group_id]]
        response = f"**╭── : [𝗧𝗲𝗠 𝗔𝗹𝗤𝗮𝗜𝗱]({soesh}) : ──╮\n\n⌁|𝗧𝗵𝗘 𝗦𝗼𝗡𝗴𝗦 𝗢𝗻 𝗧𝗵𝗘 𝗟𝗶𝗦𝘁:\n\n⌁|𝗡𝘂𝗠𝗯𝗘𝗿 𝗦𝗼𝗡𝗴𝗦: {count}\n\n**"
        if count == 0:
            return await message.reply_text("**مفيش اغاني في القائمه**")
        else:
            for user_mention in user_mentions:
                response += f"**{o}- {user_mention}\n**"
                o += 1
        await message.reply_text(response, reply_markup=InlineKeyboardMarkup(button), reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await message.reply_text("**مفيش اغاني في القائمه**")
        
@Client.on_callback_query(filters.regex(pattern=r"^(pause|skip|stop|resume)$"))
async def admin_risghts(client: Client, CallbackQuery):
    bot_username = client.me.username 
    hoss = await get_call(bot_username)
    a = await client.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     return await CallbackQuery.answer("يجب انت تكون ادمن للقيام بذلك  !", show_alert=True)
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id
    if command == "pause":
        try:
         await hoss.pause_stream(chat_id)
         await CallbackQuery.answer("تم ايقاف التشغيل موقتا .", show_alert=True)
         await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم ايقاف التشغيل بواسطه**")
        except Exception as e:
         await CallbackQuery.answer("يعم فوق مفيش حاجه شغاله 😹🎶لا", show_alert=True)
         await CallbackQuery.message.reply_text(f"**يعم فوق مفيش حاجه شغاله 😹🎶لا يا {CallbackQuery.from_user.mention}**")
    if command == "resume":
        try:
         await hoss.resume_stream(chat_id)
         await CallbackQuery.answer("تم استكمال التشغيل .", show_alert=True)
         await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم إستكمال التشغيل بواسطه**")
        except Exception as e:
         await CallbackQuery.answer("يعم فوق مفيش حاجه شغاله 😹🎶لا", show_alert=True)
         await CallbackQuery.message.reply_text(f"**يعم فوق مفيش حاجه شغاله 😹🎶لا يا {CallbackQuery.from_user.mention}**")
    if command == "stop":
       try:    	
        playlist[chat_id].clear()
        thu[chat_id].clear()
       except Exception as e:
        print(f"{e}")
       try:    	
        await hoss.leave_group_call(chat_id)
       except Exception as e:
        print(f"{e}")
       await CallbackQuery.answer("تم انهاء التشغيل بنجاح .", show_alert=True)
       await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم انهاء التشغيل بواسطه**")
    if command == "skip":
       await change_stream(bot_username, chat_id, client)
       await CallbackQuery.answer("تم تخطي التشغيل .", show_alert=True)

       
@Client.on_message(filters.command(["اسكت", "ايقاف"], "") & filters.group, group=55646568548)
async def ghuser(client, message):
    if await johned(client, message):
     return
    bot_username = client.me.username
    user = await get_userbot(bot_username) 
    hoss = await get_call(bot_username)
    group_id = message.chat.id
    chek = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chek.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.username in caes:
     chat_id = message.chat.id
     ho = await message.reply_text("**جاري ايقاف التشغيل**") 
     try:    	
      playlist[chat_id].clear()
      thu[chat_id].clear()
     except Exception as e:
      print(f"{e}")
     try:    	
      await hoss.leave_group_call(message.chat.id)
      await ho.edit_text("**حاضر سكت اهو 🥺❤**")
     except Exception as e:
      await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")    
    else:
      return await message.reply_text(f"**عذرا عزيزي{message.from_user.mention}\n هذا الامر لا يخصك✨♥**")

@Client.on_message(filters.command(["اسكت", "ايقاف", "/stop", "انهاء"], "") & filters.channel, group=5564656568548)
async def gh24user(client, message):
     bot_username = client.me.username
     user = await get_userbot(bot_username)  
     hoss = await get_call(bot_username)
     chat_id = message.chat.id
     ho = await message.reply_text("**جاري ايقاف التشغيل**") 
     try:    	
      playlist[chat_id].clear()
      thu[chat_id].clear()
     except Exception as e:
      print(f"{e}")
     try:    	
      await hoss.leave_group_call(message.chat.id)
      await ho.edit_text("**حاضر سكت اهو 🥺❤**")
     except Exception as e:
      await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")    
 
@Client.on_message(filters.command(["تخطي", "/skip"], "") & filters.group, group=5864548)
async def skip2(client, message):
    if await johned(client, message):
     return
    bot_username = client.me.username
    user = await get_userbot(bot_username) 
    hoss = await get_call(bot_username)
    group_id = message.chat.id
    chek = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chek.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.username in caes:
     chat_id = message.chat.id
     ho = await message.reply_text("**جاري تخطي التشغيل**") 
     await ho.delete()
     await change_stream(bot_username, chat_id, client)
    else:
     return await message.reply_text(f"**عذرا عزيزي{message.from_user.mention}\n هذا الامر لا يخصك✨♥**")

@Client.on_message(filters.command(["تخطي", "/skip"], "") & filters.channel, group=5869864548)
async def ski25p2(client, message):
    bot_username = client.me.username
    user = await get_userbot(bot_username)
    hoss = await get_call(bot_username)
    chat_id = message.chat.id
    ho = await message.reply_text("**جاري تخطي التشغيل**") 
    await ho.delete()
    await change_stream(bot_username, chat_id, client)
    
@Client.on_message(filters.command(["توقف", "وقف"], "") & filters.group, group=58655654548)
async def sp2(client, message):
    if await johned(client, message):
     return
    bot_username = client.me.username
    hoss = await get_call(bot_username)
    group_id = message.chat.id
    chek = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chek.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.username in caes:
     chat_id = message.chat.id
     ho = await message.reply_text("**هوقف كلام حاضر ✨🔊**") 
     try:    	
      await hoss.pause_stream(chat_id)
      await ho.edit_text("**وقفت كلام اهو 😞🔇**")
     except Exception as e:
      await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")
    else:
     return await message.reply_text(f"**عذرا عزيزي{message.from_user.mention}\n هذا الامر لا يخصك✨♥**")

@Client.on_message(filters.command(["توقف", "وقف"], "") & filters.channel, group=5866555654548)
async def s356p2(client, message):
    bot_username = client.me.username
    hoss = await get_call(bot_username)
    chat_id = message.chat.id
    ho = await message.reply_text("**هوقف كلام حاضر ✨🔊**") 
    try:    	
     await hoss.pause_stream(chat_id)
     await ho.edit_text("**وقفت كلام اهو 😞🔇**")
    except Exception as e:
     await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")
     
@Client.on_message(filters.command(["كمل"], "") & filters.group, group=5866564548)
async def s12p2(client, message):
    if await johned(client, message):
     return
    bot_username = client.me.username
    hoss = await get_call(bot_username)
    group_id = message.chat.id
    chek = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chek.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.username in caes:
     chat_id = message.chat.id
     ho = await message.reply_text("**خلاص هكمل التشغيل يروحي ♥🥰**") 
     try:    	
      await hoss.resume_stream(chat_id)
      await ho.edit_text("**خلاص اشتغلت يروحي ✨🥰**")
     except Exception as e:
      await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")
    else:
     return await message.reply_text(f"**عذرا عزيزي{message.from_user.mention}\n هذا الامر لا يخصك✨♥**")

@Client.on_message(filters.command(["كمل"], "") & filters.channel, group=645866564548)
async def s12p582(client, message):
    bot_username = client.me.username
    hoss = await get_call(bot_username)
    chat_id = message.chat.id
    ho = await message.reply_text("**خلاص هكمل التشغيل يروحي ♥🥰**") 
    try:    	
     await hoss.resume_stream(chat_id)
     await ho.edit_text("**خلاص اشتغلت يروحي ✨🥰**")
    except Exception as e:
     await ho.edit_text("**يعم فوق مفيش حاجه شغاله 😹🎶لا**")