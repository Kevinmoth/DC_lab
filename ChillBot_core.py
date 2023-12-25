import discord
from discord.ext import commands
from discord import Interaction
import random
import os
import asyncio


intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.guilds = True

current_song_index = 0
playlist = []

client = commands.Bot(command_prefix=".", intents= discord.Intents.all())

@client.event
async def on_ready():
	print(f"{client.user.name} está iniciando sesión ")
	game = discord.Game("¡Guanabana!")
    # Establecer el estado
	await client.change_presence(activity=game)
    
    
target_channel_id = 937112558094155847

@client.command()
async def hola(ctx):
    await ctx.send("Buenas!")

@client.command()
async def play(ctx):
    global playlist
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

        music_files = ["music.ogg", "music2.mp3", "music3.mp3"]
        random.shuffle(music_files)
        playlist.extend(music_files)

        await ctx.send(f'ChillBot entró al canal: {channel.name} :mate: ')

        while playlist:
            audio_file = playlist.pop(0)
            if os.path.exists(audio_file):
                voice_channel.play(
                    discord.FFmpegPCMAudio(audio_file, executable="ffmpeg", options="-vn -b:a 192k"),
                    after=lambda e: print('done', e)
                )
                while voice_channel.is_playing():
                    await asyncio.sleep(1)
            else:
                await ctx.send(f'Archivo no encontrado: {audio_file}')

        await voice_channel.disconnect()
    else:
        await ctx.send('Debes estar en un canal de voz para usar este comando.')
        
@client.command()
async def next(ctx):
    global current_song_index, playlist
    if current_song_index < len(playlist):
        await ctx.send(' :mate: Pasando...')
        current_song_index += 1

        if ctx.voice_client.is_playing():
            # Detener la reproducción actual antes de pasar a la siguiente canción
            ctx.voice_client.stop()

        # Verificar si current_song_index excede los límites de la lista
        if current_song_index < len(playlist):
            next_song = playlist[current_song_index]

            # Reproducir la siguiente canción
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(next_song, executable="ffmpeg", options="-vn -b:a 192k -t 600"),
                after=lambda e: print('done', e)
            )
        else:
            current_song_index = 0
    else:
        await ctx.send('No hay más canciones en la lista.')
    
        

    
@client.command()
async def unir(ctx):
    channel_id = 937112558094155847  
    
    channel = client.get_channel(channel_id)
    if channel:
        
        voice_channel = await channel.connect()
        
        audio_file = "music.ogg" 
        voice_channel.play(discord.FFmpegPCMAudio(audio_file, executable="ffmpeg", options="-vn -b:a 192k"), after=lambda e: print('done', e))
        await ctx.send(f'ChillBot entro al canal : {channel.name}')
    else:
        await ctx.send('No se pudo encontrar el canal de voz.')
        
@client.command()
async def salir(ctx):
    
    await ctx.voice_client.disconnect()
    await ctx.send('Bot desconectado del canal de voz.')

client.run("Token")



