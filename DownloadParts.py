from pytube import YouTube
from pathlib import Path
import os
from pytube import Playlist
from pytube import Channel
import ffmpeg




def mk_vdir(foldername):
    path= f"{foldername}"
    Path(path).mkdir(parents=True, exist_ok=True)




def replace_invalid(text:str):
    not_allowed=["/",":","?","*",">","<","|"," ","\\"]
    for i in not_allowed:
        text=text.replace(i,"_")
        
    text= text+".mp4"
    
    return text




def video_download(url, foldername):
    mk_vdir(foldername)
    
    yt = YouTube(url)
    video_title= yt.title
   
    title= replace_invalid(yt.title)
    
    
    stream = yt.streams.get_highest_resolution()
    if len(video_title)>=50:
        video_title=video_title[:50]
    
    stream.download(foldername, filename=title)
    
    return title, video_title






def audio_download(url, foldername):

    mk_vdir(foldername)
    
    yt = YouTube(url)
    
    title= replace_invalid(yt.title)
    stream_audio = yt.streams.get_by_itag(140)
    stream_audio.download(foldername, filename=title)
    
    return title






def playlist_download(url, foldername, type_="video"):
    mk_vdir(foldername)
    
    title_list = []

    p = Playlist(url)
    if type_=="audio":
        for video in p.videos:
            title= replace_invalid(video.title)
            title_list.append(title)
            video.streams.get_by_itag(140).download(filename=title)
    elif type_=="video":
        for video in p.videos:
            stream=video.streams.get_highest_resolution()
            title= replace_invalid(video.title)
    
            title_list.append(title)
            stream.download(foldername, filename=title)
    else:
        print("failed to download!")
    
    return title_list




      
def get_playlist(url):
    
    results=[]
    
    
    p = Playlist(url)
    for v in p.videos:
        
        vid=v.video_id
        url=v.watch_url
        if len(v.title)>=50:
            title=v.title[:50]
        else:
            title=v.title
        results.append({
            "vid":vid,
            "title":title,
            "url":url,
            
        })
        
    return results




def channel_download(url, foldername):
    mk_vdir(foldername)
    c = Channel(url)
    Channel_title=c.title
    
    for video in c.videos:
        stream=video.streams.get_highest_resolution()
        title= replace_invalid(video.title)
    
        stream.download(foldername, filename=title)

    return Channel_title






def convert_to_mp3(foldername, filename)->str:

    new_filename=filename[:-3]+"mp3"
    if filename[-3:]=="mp4":
    
        (
            ffmpeg.input(os.path.join(foldername, filename))
            .output(os.path.join(foldername, new_filename))
            .run(overwrite_output=True)
        )
        os.remove(os.path.join(foldername, filename))
        
    return new_filename





def mp3_download(url, foldername)->str:
    
    filename=audio_download(url, foldername)
    new_filename=convert_to_mp3(foldername, filename)
    
    return new_filename





def cut_video(dirname, start_t, end_t, filename=None):

    if filename:
        input_ = os.path.join(dirname, filename)
        new_filename="cut_"+filename
        output = os.path.join(dirname, new_filename)
        os.system(f"ffmpeg -i {input_} -ss {start_t} -to {end_t} -vcodec copy -acodec copy {output}")
        return new_filename
    

    for filename in os.listdir(dirname):
        if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
            input_ = os.path.join(dirname, filename)
            new_filename="cut_"+filename
            output = os.path.join(dirname, new_filename)
            os.system(f"ffmpeg -i {input_} -ss {start_t} -to {end_t} -vcodec copy -acodec copy {output}")
            return new_filename
        else:
            continue
        
    
    
    
    
    
    
    
    
    
    
    
