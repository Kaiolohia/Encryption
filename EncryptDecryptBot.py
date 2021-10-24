import discord
import EncryptDecryptV4_C 
import BotTokens

ED = EncryptDecryptV4_C.EncryptDecrypt()

client = discord.Client()

@client.event
async def on_ready():
  print('Bot up and running')

@client.event
async def on_message(message):
  encryptThis = ''
  decryptThis = ''
  
  if message.author == client.user:
    return
  
  if message.content.startswith('|encrypt'):
    messageUnstructored = str(message.content).split(' ')
    messageUnstructored.pop(0)
    messageUnstructored = [x + ' ' for x in messageUnstructored]

    for i in range(len(messageUnstructored)):
      encryptThis = encryptThis + messageUnstructored[i]
    
    embedEncrypt = discord.Embed(title = 'Encrypted message:', description = str(ED.encrypt(encryptThis)), color = 0x36F95D)
    embedEncrypt.set_footer(text = 'Developed by Trux#0001')

    await message.channel.send(embed = embedEncrypt)

    try:
      await message.delete()
    except:
      print('Delete Failed')

  if message.content.startswith('|decrypt'):
    messageUnstructored = str(message.content).split(' ')
    messageUnstructored.pop(0)

    for i in range(len(messageUnstructored)):
      decryptThis = messageUnstructored[i]

    decryptedEmbed = discord.Embed(title = 'Your decrypted message:', description = ED.decrypt(decryptThis), color = 0x36F95D)
    decryptedEmbed.set_footer(text = 'Developed by Trux#0001')

    await message.channel.send(embed = decryptedEmbed)

    try:
      await message.delete()
    except:
      pass

  if message.content.startswith('|help'):
    await message.channel.send('**Commands**\n|encrypt (message) | Encrypts your message using the bots custom encryption method\n|decrypt (message) | Decrypts the bots encrypted messages')
    
    try:
      await message.delete()
    except:
      pass

client.run(BotTokens.Encrypt())