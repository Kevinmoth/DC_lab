import discord
from discord.ext import commands
from discord import Interaction

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.guilds = True

client = commands.Bot(command_prefix=".", intents= discord.Intents.all())

@client.event
async def on_ready():
	print(f"{client.user.name} está iniciando sesión ")
	game = discord.Game("¡Guanabana!")
	await client.change_presence(activity=game)
    
    
target_channel_id = 937112558094155847

@client.command()
async def hola(ctx):
    await ctx.send("Buenas!")
    
@client.command()
async def unir(ctx):
    channel_id = 937112558094155847  
    
    channel = client.get_channel(channel_id)
    if channel:
        # Unir al bot al canal de voz
        voice_channel = await channel.connect()
        # Reproducir el archivo de audio en bucle
        audio_file = "music.ogg"  
        voice_channel.play(discord.FFmpegPCMAudio(audio_file, executable="ffmpeg", options="-vn -b:a 192k"), after=lambda e: print('done', e))
        await ctx.send(f'Bot unido al canal de voz: {channel.name}')
    else:
        await ctx.send('No se pudo encontrar el canal de voz.')
        
@client.command()
async def salir(ctx):
    # Desconectar al bot del canal
    await ctx.voice_client.disconnect()
    await ctx.send('Bot desconectado del canal de voz.')

client.run("Token")



