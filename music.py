import discord
from discord.ext import commands
from discord import Interaction

client = commands.Bot(command_prefix=".", intents= discord.Intents.all())

@client.event
async def on_ready():
	print(f"{client.user.name} está iniciando sesión ")
target_channel_id = 937112558094155847
@client.command()
async def hola(ctx):
    await ctx.send("Buenas!")
    
@client.command()
async def unir(ctx):
    channel_id = 937112558094155847  # ID del canal de voz al que quieres unirte

    # Obtener el objeto de canal de voz
    channel = client.get_channel(channel_id)

    if channel:
        # Unir al bot al canal de voz
        voice_channel = await channel.connect()

        # Reproducir un archivo de audio en bucle
        audio_file = "music.ogg"  # Reemplaza con el nombre de tu archivo .ogg
        voice_channel.play(discord.FFmpegPCMAudio(audio_file, executable="ffmpeg", options="-vn -b:a 192k"), after=lambda e: print('done', e))

        await ctx.send(f'Bot unido al canal de voz: {channel.name}')
    else:
        await ctx.send('No se pudo encontrar el canal de voz.')

@client.command()
async def salir(ctx):
    # Desconectar al bot del canal de voz actual
    await ctx.voice_client.disconnect()
    await ctx.send('Bot desconectado del canal de voz.')

    

client.run("MTE4MjgyNTYxNjQxNjk2ODcxNA.GM4oX0.8G1simtGMjxq_1KiWp8dShd_5x84Pa5AjHmHDU")



