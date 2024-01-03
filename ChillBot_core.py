import discord
from discord.ext import commands
from discord import Interaction
import random
import os
import asyncio
import youtube_dl

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.guilds = True

current_song_index = 0
playlist = []
gif_link = "https://cdn.discordapp.com/emojis/936786898905628702.gif?size=96&quality=lossless"

client = commands.Bot(command_prefix=".", intents= discord.Intents.all())

@client.event
async def on_ready():
	print(f"{client.user.name} está iniciando sesión ")
	game = discord.Game("¡Guanabana!")
    
	await client.change_presence(activity=game)
    
    
target_channel_id = 1149127509657526362


@client.command()
async def play_(ctx, *, query_or_url):
    global playlist
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None

    if voice_channel:
        if ctx.voice_client:
            if ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
        else:
            voice_client = await voice_channel.connect()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
                'preferredquality': '64',  
            }],
            'outtmpl': 'song.mp3',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in query_or_url or "youtu.be" in query_or_url:
                info = ydl.extract_info(query_or_url, download=False)
                title = info['title']
                url = info['url']
            else:
                info = ydl.extract_info(f"ytsearch:{query_or_url}", download=False)
                title = info['entries'][0]['title'] if 'entries' in info else info['title']
                url = info['entries'][0]['url'] if 'entries' in info else info['url']

            playlist.append(url)
            await ctx.send(f' :mate: Canción añadida a la lista de reproducción: {title}')

            try:
                emoji_id = 951309958727753788  
                emoji = client.get_emoji(emoji_id)
                if emoji:
                    await ctx.message.add_reaction(emoji)
            except:
                pass

            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await play_next(ctx, ctx.voice_client)
    else:
        await ctx.send(' :mate: Debes estar en un canal de voz para usar este comando.')



async def play_next(ctx, voice_channel):
    global playlist
    if playlist:
        url = playlist.pop(0)
        voice_channel.play(discord.FFmpegPCMAudio(url, executable="ffmpeg", options="-vn -b:a 192k"), after=lambda e: asyncio.run(play_next(ctx, voice_channel)))
        await ctx.send(f' :mate: Reproduciendo: {title}')
    else:
        await voice_channel.disconnect()
@client.command()
async def hola(ctx):
    await ctx.send("Buenas!")

@client.command()
async def play(ctx):
    global playlist
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

        music_files = ["music.ogg", "music2.mp3", "music3.mp3", "music4.mp3"]
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

       
    else:
        await ctx.send('Debes estar en un canal de voz para usar este comando.')
        
@client.command()
async def next(ctx):
    global current_song_index, playlist
    if current_song_index < len(playlist):
        await ctx.send(' :mate: Pasando...')
        current_song_index += 1

        if ctx.voice_client.is_playing():
           
            ctx.voice_client.stop()

      
        if current_song_index < len(playlist):
            next_song = playlist[current_song_index]

          
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

client.run("token")

