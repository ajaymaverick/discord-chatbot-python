'''
Flask App to provide google search and search through recent searches
done by user on discord chat app

@author: ajay
'''

import os

import discord
from dotenv import load_dotenv

from flask import Flask
from database import db
import controller as controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://afeejhtaymlybr:b5bef6c9c889b5c38a1816960333f115b5062c9eed76192ec1689af379011b97@ec2-107-21-214-26.compute-1.amazonaws.com:5432/d7s96eafqhstgn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()

db.create_all()

# Load credentials to for discord client
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Default response to be provided by chatbot
    response = 'I cannot understand, please try again'
    
    # If users says hi, then send hey as response 
    if message.content == 'hi':
        response = 'hey'
        
    # Provides functionality to allow a user to search on google through discord    
    if message.content.startswith('!google'):
        query = message.content.replace('!google', '')
        if(len(query.strip()) > 0):
            response =  controller.getGoogleSearchResult(query)
            controller.storeSearchHistory(message.author.name,query)
        else:
            response = 'Invalid input, please provide search query'
        
    #Provides functionality to search through user's search history, returns most recent searches   
    if message.content.startswith('!recent'):
        query = message.content.replace('!recent', '')
        if(len(query.strip()) > 0):
            response = controller.getSearchHistory(message.author.name, query)
        else:
            response = 'Invalid input, please provide search query'
    
    
    await message.channel.send(response)

client.run(token)

@app.route('/')
def index():
    return 'Welcome to discord chatbot '


if __name__ == '__main__':
    app.run(threaded=True)


    
