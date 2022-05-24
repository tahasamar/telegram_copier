from pyrogram import Client,filters
from pyrogram.types import Message,InputMediaPhoto,InputMediaVideo,InputMediaAnimation,InputMediaAudio,InputMediaDocument
import pickle
import os
from filelock import FileLock
import time

#put your api id and api hash here . find them here : my.telegram.org
api_id=00
api_hash="--"

app=Client("bot",api_id,api_hash)

@app.on_deleted_messages(filters.channel)
def deleted(bot:Client,msgs:Message):

    with open("chans.pkl","rb") as f:
        chans=pickle.load(f)
    for msg in msgs: 
        if not str(msg.chat.id) in chans:
            return  
        if not os.path.exists(f"msg-{msg.chat.id}.pkl"):
            with open(f"msg-{msg.chat.id}.pkl","wb") as f:
                pickle.dump({},f)
                return
        with open(f"msg-{msg.chat.id}.pkl","rb") as f:
            d=pickle.load(f)
        if msg.id in d:
            bot.delete_messages(chans[str(msg.chat.id)],d[msg.id])

@app.on_edited_message(filters.channel)
async def edit(bot :Client,msg:Message):

    with open("chans.pkl","rb") as f:
        chans=pickle.load(f)

    if not str(msg.chat.id) in chans:
        return
    #check if msg-msg.chat.id file exists and if not create it
    #else load the pickle and find the msg.id in the dict as edited_message
    #edit the message with id as edited_message 
    if not os.path.exists(f"msg-{msg.chat.id}.pkl"):
        with open(f"msg-{msg.chat.id}.pkl","wb") as f:
            pickle.dump({},f)
    with open(f"msg-{msg.chat.id}.pkl","rb") as f:
        d=pickle.load(f)
    if msg.id in d:
        # if msg.chat.has_protected_content:
        if msg.chat.has_protected_content:
            b=None
            if msg.text:
                await bot.edit_message_text(text=msg.text,chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.photo:
                b=await bot.download_media(msg.photo)
                await bot.edit_message_media(media=InputMediaPhoto(b,msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.video:
                b=await bot.download_media(msg.video)
                await bot.edit_message_media(media=InputMediaVideo(b,msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.audio:
                b=await bot.download_media(msg.audio)
                await bot.edit_message_media(media=InputMediaAudio(b,caption=msg.caption,caption_entities=msg.caption_entities,duration=msg.audio.duration,performer=msg.audio.performer,title=msg.audio.performer),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.document:
                b=await bot.download_media(msg.document)
                await bot.edit_message_media(media=InputMediaDocument(b,caption=msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            else:
                await bot.edit_message_caption(chans[str(msg.chat.id)],d[msg.id],msg.caption)
            if b:os.remove(b)        
        else:
            if msg.text:
                await bot.edit_message_text(text=msg.text,chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.photo:
                await bot.edit_message_media(media=InputMediaPhoto(msg.photo.file_id,msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.video:
                await bot.edit_message_media(media=InputMediaVideo(msg.video.file_id,msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.audio:
                await bot.edit_message_media(media=InputMediaAudio(msg.audio.file_id,caption=msg.caption,caption_entities=msg.caption_entities,duration=msg.audio.duration,performer=msg.audio.performer,title=msg.audio.performer),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            elif msg.document:
                await bot.edit_message_media(media=InputMediaDocument(msg.document.file_id,caption=msg.caption,caption_entities=msg.caption_entities),chat_id=chans[str(msg.chat.id)],message_id=d[msg.id])
            else:
                await bot.edit_message_caption(chans[str(msg.chat.id)],d[msg.id],msg.caption)
            

@app.on_message(filters.channel)
async def all(bot : Client,msg : Message):
    # get the chans pickle file and load it as dict search for chat.id in the keys 
    # if found then send the message to the channel
    with open("chans.pkl","rb") as f:
        chans=pickle.load(f)
    # print(msg.chat.id)
    if not str(msg.chat.id) in chans:
        return

    # check if msg-<msg.chat.id> file pickle exists and find the msg.id in the file 
    # if found , reply the messages to the accourding msg id in the file 
    #if file does not exist then create a new file and add the msg.id to the file

    if not os.path.exists("msg-"+str(msg.chat.id)+".pkl"):
        with open("msg-"+str(msg.chat.id)+".pkl","wb") as f:
            pickle.dump({"":""},f)
    with open(f"msg-{msg.chat.id}.pkl","rb") as f:
        msgs=pickle.load(f)
    print(msgs)
    if msg.reply_to_message_id and (msg.reply_to_message_id) in msgs:
        reply = msgs[(msg.reply_to_message_id)]
    else:
        reply=None  
    print(reply)
    
        
    if msg.chat.has_protected_content:
        b=None
        if msg.text:    
            sent=await bot.copy_message(chans[str(msg.chat.id)],msg.chat.id,msg.id,reply_to_message_id=reply)
        elif msg.photo:
            b=await bot.download_media(msg.photo)
            sent=await bot.send_photo(chans[str(msg.chat.id)],b,caption=msg.caption,caption_entities=msg.caption_entities , reply_to_message_id=reply)
            # print("media")
        elif msg.video:
            b=await bot.download_media(msg.video)
            sent=await bot.send_video(chans[str(msg.chat.id)],b,caption=msg.caption,caption_entities=msg.caption_entities , reply_to_message_id=reply)
            # print("video")
        elif msg.audio:
            b=await bot.download_media(msg.audio)
            sent=await bot.send_audio(chans[str(msg.chat.id)],b,caption=msg.caption,caption_entities=msg.caption_entities , reply_to_message_id=reply)
            # print("audio")
        elif msg.voice:
            b=await bot.download_media(msg.voice)
            sent=await bot.send_voice(chans[str(msg.chat.id)],b,caption=msg.caption,caption_entities=msg.caption_entities , reply_to_message_id=reply)
            # print("voice")
        elif msg.document:
            b=await bot.download_media(msg.document)
            sent=await bot.send_document(chans[str(msg.chat.id)],b,caption=msg.caption,caption_entities=msg.caption_entities , reply_to_message_id=reply)
            # print("document")
        elif msg.sticker:
            b=await bot.download_media(msg.sticker)
            # print("sticker")
            sent=await bot.send_sticker(chans[str(msg.chat.id)],b , reply_to_message_id=reply)
        elif msg.animation:
            b=await bot.download_media(msg.animation)
            sent=await bot.send_animation(chans[str(msg.chat.id)],b , reply_to_message_id=reply)
            # print("animation")
        elif msg.video_note:
            b=await bot.download_media(msg.video_note)
            sent=await bot.send_video_note(chans[str(msg.chat.id)],b , reply_to_message_id=reply)
            # print("video_note")
        elif msg.contact:
            sent=await bot.send_contact(chans[str(msg.chat.id)],msg.contact.phone_number,msg.contact.first_name,msg.contact.last_name,msg.contact.user_id,msg.contact.vcard , reply_to_message_id=reply)
            # print("contact")
        elif msg.location:
            sent=await bot.send_location(chans[str(msg.chat.id)],msg.location.latitude,msg.location.longitude , reply_to_message_id=reply)
            # print("location")
        elif msg.venue:
            sent=await bot.send_venue(chans[str(msg.chat.id)],msg.venue.location.latitude,msg.venue.location.longitude,msg.venue.title,msg.venue.address , reply_to_message_id=reply)
            # print("venue")
        elif msg.game:
            sent=await bot.send_game(chans[str(msg.chat.id)],msg.game.title,msg.game.description,msg.game.animation , reply_to_message_id=reply)
            # print("game")
        if b:
            os.remove(b)
    else:
        sent=await bot.copy_message(chans[str(msg.chat.id)],msg.chat.id,msg.id,reply_to_message_id=reply)
    
    # open the file and save the sent message id in for the msg.id
    with open(f"msg-{msg.chat.id}.pkl","wb") as f:
        msgs[(msg.id)]=sent.id
        # print(msgs)
        pickle.dump(msgs,f)

@app.on_message(filters.create(lambda f,bot,msg: msg.chat.id==bot.get_me().id and msg.text))
def private(bot : Client,msg:Message):
    if msg.forward_from_chat:
        bot.send_message(msg.chat.id,msg.forward_from_chat.id)
    # if the message text is "add" then add the chat.id to the chans pickle file
    # if the message text is "del" then delete the chat.id from the chans pickle file
    # if the message text is "list" then list the chat.id in the chans pickle file
    if not os.path.exists("chans.pkl"):
        with open("chans.pkl","wb") as f:
            pickle.dump({"":""},f)
    if msg.text[:3]=="add":
        with open("chans.pkl","rb") as f:
            chans=pickle.load(f)
        chans[msg.text.split(":")[0].replace("add","").replace(" ","")]=msg.text.split(":")[1].replace(" ","")
        with open("chans.pkl","wb") as f:
            pickle.dump(chans,f)
        bot.send_message(msg.chat.id,"added")
    elif msg.text[:3]=="del":
        with open("chans.pkl","rb") as f:
            chans=pickle.load(f)
        if msg.text.split("del")[1].replace(" ","") in chans:
            # print(chans)
            # print(msg.text.split("del")[1])
            del chans[msg.text.split("del")[1].replace(" ","")]
            # print(chans)
            with open("chans.pkl","wb") as f:
                pickle.dump(chans,f)
            bot.send_message("me","deleted")
    elif msg.text=="list":
        with open("chans.pkl","rb") as f:
            chans=pickle.load(f)
        bot.send_message(msg.chat.id,"\n".join(["-"]+[key+"->"+chans[key] for key in chans]))

app.run()
