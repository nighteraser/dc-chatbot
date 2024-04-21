import discord
import traceback
from openai import OpenAI
from discord import app_commands
from discord.ext import commands
from typing import Optional

# model = 'mistral'
model = 'yabi/breeze-7b-instruct-v1_0_q6_k'
ai_character_path = './lore.txt'
lore = ''
message_log = []
character_limit = 3000
language = 'en'

client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

def init_chatbot():
    global message_log, lore
    try:
        with open(ai_character_path, "r", encoding="utf-8") as file:
            lore = file.read()
    except:
        print("error when reading lore.txt")
        print(traceback.format_exc())
    lore = lore.replace('\n', ' ')
    message_log = [{'role': 'system', 'content': lore}]

init_chatbot()

def send_user_input(user_input):
    global chat_model, message_log
    
    print(f'Sending: {user_input}')
    message_log.append({"role": "user", "content": user_input})
    print(message_log)
    total_characters = sum(len(message['content']) for message in message_log)
    print(f"total_characters: {total_characters}")
    while total_characters > character_limit and len(message_log) > 1:
        print(f"total_characters {total_characters} exceed limit of {character_limit}, removing oldest message")
        total_characters -= len(message_log[1]["content"])
        message_log.pop(1)
        
    print("loading...")
    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=message_log,
            temperature=0.9, # high temperature more creative
        )
    except:
        return
    
    text_response = chat_completion.choices[0].message.content
    print(f'\033[1;34mAI: {text_response}\033[0m')
    message_log.append({"role": "assistant", "content": text_response})
    return text_response

def change_chat_model(model):
    global chat_model
    chat_model = model
    init_chatbot()

async def set_system_context(text):
    global lore, message_log
    lore = text
    lore = lore.replace('\n', ' ')
    print('clean up history...')
    message_log = [{'role': 'system', 'content': lore}]

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "chat", description = "chat with ai bot")
    @app_commands.describe(text = "User said: ")

    async def chat(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f'{interaction.user}: **{text}**')
        await interaction.followup.send(send_user_input(text))  

    @app_commands.command(name = "set", description = "set AI system")
    @app_commands.describe(text = "text something what you want ai to be")

    async def set(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f'{interaction.user} set AI: \n**{text}**')
        await set_system_context(text)

    @app_commands.command(name = "show", description = "show ai system (charater, lore)")
    
    async def show(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'System: \n**{lore}**')


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))