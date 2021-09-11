from pytgcalls import GroupCallFactory as gcf
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import config
from misc import url_stream, ytsearch, user_input, streamloop, thumbnail, title
from os import path
import asyncio
# PYROGRAM CLIENT

app = Client(config.STRING_SESSION, api_id = config.API_ID, api_hash = config.API_HASH)
bot = Client("bot", api_id = config.API_ID, api_hash = config.API_HASH, bot_token = config.BOT_TOKEN)
que = asyncio.Queue()
# PYTGCALLS CLIENT

Calls = gcf(app).get_group_call()

loop = asyncio.get_event_loop()

async def init():
    await app.start()
    print("User Client Started!")
    await bot.start()
    print("Bot Client Started!")
    admins = 133
    @bot.on_message(filters.command("alive"))
    async def startxd(client, message):
        await message.reply("Yes I am Alive!,Who cares about someone else!")
    @bot.on_message(filters.command(["start", "help"]) & filters.private)
    async def start(client, message):
        sender_mention = message.from_user.mention
        await message.reply(f"Hi! {sender_mention}, This is a video streaming bot. Here is a link to my source code!", reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = "Repository",
                        url = "https://github.com/VegetaxD/VideoStreamBot"                  
                    )                
                ]
            ]
                    )
                            )
    @bot.on_message(filters.command("vplay") & filters.chat(config.VIDEO_CHAT_ID)) 
    async def stream(client, message):
        user_str = await user_input(message.text)
        if Calls.is_running:
            number = 0
            next_vid = (user_str)
            await que.put(next_vid)
            number += 1
            return await message.reply(f"Added **Video🎥 : __{next_vid}__** To Queue!\n\n**Queued at #{number}**")
        if not user_str:
            await message.reply("Please give a youtube link/keyword to stream!")
        else:
            process = await message.reply("Processing!")
            video = await streamloop(user_str)    
        try:
            await process.edit("Starting Streaming!")        
            await process.delete()
            await Calls.join(message.chat.id)
            playout = await Calls.start_video(video, repeat=False)
            thumb = thumbnail(user_str)
            namee = title(user_str)
            await message.reply_photo(thumb, caption = f"Started Streaming!\n\n**Video🎥** : **__{namee}__**\n**Chat : {message.chat.title}**\n**Requested By : {message.from_user.mention}**")
        except Exception as e:
            return await message.reply(e)
        @Calls.on_playout_ended
        async def media_ended(_, source, media_type):
            return await message.reply_text(f"Finished Media Type: {media_type}")
        
   
    @bot.on_message(filters.command("repo") ) 
    async def repo(client, message):
        return await message.reply("Here is the Repository!", reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = "Repository",
                        url = "https://github.com/VegetaxD/VideoStreamBot"
                    )                
                ]
            ]
                    )
                            )
    
    @bot.on_message(filters.command("vstop") & filters.user(admins) & filters.chat(config.VIDEO_CHAT_ID) ) 
    async def pause(client, message):
        await Calls.stop()
        return await message.reply("The Video Has Been Stopped Successfully!")
    
    @bot.on_message(filters.command("vpause") & filters.user(admins) & filters.chat(config.VIDEO_CHAT_ID) ) 
    async def pause(client, message):
        await Calls.set_pause(True)
        return await message.reply("The Video Has Been Paused ⏸ Successfully!")
    
    @bot.on_message(filters.command("vresume") & filters.user(admins) & filters.chat(config.VIDEO_CHAT_ID)) 
    async def resume(client, message):
        await Calls.set_pause(False)
        return await message.reply("The Video Has Been Resumed ▶️ Successfully!")

    @bot.on_message(filters.command("vskip") & filters.user(admins) & filters.chat(config.VIDEO_CHAT_ID)) 
    async def skip(client, message):
        if que.empty():
            await message.reply("No More Videos In Queue!\n\nLeaving Video Chat! xD")
            return await Calls.stop()
        else:
            process = await message.reply("Processing!")
            stuff = await que.get()
            
        try:
            video = await streamloop(stuff)
            await process.delete()
            await Calls.join(message.chat.id)
            await Calls.start_video(video, repeat=False)
            thumb = thumbnail(stuff)
            namee = title(stuff)
            return await message.reply_photo(photo = thumb, caption = f"Started Streaming!\n\n**Video🎥** : **__{namee}__**\n**Chat : {message.chat.title}**\n**Requested By : {message.from_user.mention}**")
        except Exception as e:
            return await message.reply(e)
    await idle()
if __name__ == '__main__':
    loop.run_until_complete(init())

# To Do
# Multiple Chats (Needs High Specs)
# Add Local Telegram Video Play
# Interactive UI
# current/Queue 
