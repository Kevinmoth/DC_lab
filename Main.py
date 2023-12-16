import discord
import random
import asyncio
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='x', intents=discord.Intents.default())

guild_id = 765279392137871400
channel_id = 906646235904082012

frases = ["Frase 1", "Frase 2", "Frase 3", "Frase 4"]  # Agrega las frases que quieras aquí

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print("Conectado")
    # Iniciar el temporizador para ejecutar la función cada 2 minutos
    responder_temporizador.start()

@tasks.loop(minutes=2)
async def responder_temporizador():
    # Obtener el canal del servidor
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    # Obtener una frase aleatoria de la lista
    frase_aleatoria = random.choice(frases)

    # Mandar el mensaje por el canal
    await channel.send(frase_aleatoria)

@bot.event
async def on_message(message):
    # Verificar que el mensaje no proviene del propio bot ni de un bot en general
    if message.author.bot:
        return

    # Puedes agregar aquí más lógica para responder al mensaje original si es necesario
    # await message.channel.send("¡Hola! He visto tu mensaje.")

    # Asegúrate de llamar al evento original para que otros eventos también se manejen correctamente
    await bot.process_commands(message)

bot.run("token")
