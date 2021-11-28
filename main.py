import discord
import os

client = discord.Client()

names = [] #stores names of those participating
signup_emoji = '\N{THUMBS UP SIGN}'
signup_message = 'a' #palce holder for message

#assigns secret santas
def assign_names():
  global names

  dic = {}

  for name in names:
    reciever = await client.get_user_info(name.id)
    reciever_name = reciever.name
    dic[name] = reciever_name
    #randomly pick names and add them, make sure no duplicates

  #checks if someone is giving to themselves
  for name in names:
    user = await client.get_user_info(name.id)
    username = user.name
    if dic[name] == username:
      #creates a new dictionary
      dic = assign_names()

  return (dic)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user):
  message = reaction.message
  emoji = reaction.emoji

  #Reacted to the signup message
  if (message == signup_message and emoji == signup_emoji):
    global names
    names.append(user.id)
    await message.channel.send('{} is in!'.format(user.name))

#This does work for some reason
@client.event
async def on_reaction_remove(reaction, user):
  message = reaction.message
  emoji = reaction.emoji

  #Reacted to the signup message
  if (message == signup_message and emoji == signup_emoji):
    global names
    print(user.id)
    names.remove(user.id)
    await message.channel.send('{} decided against joining'.format(user.name))


@client.event
async def on_message(message):
  #checks if the bot sent the message
  if message.author == client:
    return

  global names

  if message.content.startswith('$$signup'):
    #resets the list of names
    names = []

    #creates a message for users to sign up with adn saves it
    global signup_message
    signup_message = await message.channel.send('React to this message with \N{THUMBS UP SIGN} to sign up for the secret santa')

  if message.content.startswith('$$see'):
    for name in names:
      print(name)

  if message.content.startswith('$$drawnames'):

    santas = assign_names()

    # global names
    # for name in names:
    #   user = await client.get_user_info(name.id)
    #   await client.send_message(user, 'The person you are buying for is {}'.format(santas[user.name]))

    await message.channel.send('Names have been drawn, please check your DMs')
    await message.channel.send('All of those participating can send a wishlist in this channel')

client.run(os.environ['TOKEN'])