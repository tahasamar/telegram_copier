# telegram_copier
automatic copy telegram channel posts to another channel

## how to use :
edit the bot.py file and enter you api_id and api_hesh from my.telegram.org 
install `pyrogram` and `tgcrypto` usint pip (pip install pyrogram tgcrypto)
run the script (python bot.py)
the script will ask for your mobile number and verify your telegram account
you can use these commands in your `saved messages` :
  `add<first_channel_id>:<second_channel_id>` -> add a cupple of channels so messages sent to the first channel will be copied to the second channel
  `del<first_channel_id> -> removes the cupple of channels by the given first_channel_id
  `list` -> gives the list of added channels
 
 every message sent to the first channel will be copied to the sencond channel .editing and deleting a message will affect the copied message
