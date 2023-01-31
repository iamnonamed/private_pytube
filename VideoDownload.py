import DownloadParts
import os






def download(url, type_="video"):
    
    if "https://" not in url:
        return -1,-1
    elif "youtube" not in url:
        return -1, -1

    dirname="data"
    
    
    try:
    
        if type_=="audio":
            foldername=os.path.join(dirname, "audio")
            filename=DownloadParts.mp3_download(url, foldername)
            route=os.path.join(foldername, filename)
            return route
            
        elif type_=="video":
            try:
                foldername=os.path.join(dirname, "video")
                
                filename, title=DownloadParts.video_download(url, foldername)
                route=os.path.join(foldername, filename)
                
                return route, title
            except:
                return -1, -1
        else:
            return -1, -1
        
    except:
        return -1, -1



def partial_extract(route, start, end):
    
    
    dirname="data"
    
    foldername = os.path.join(dirname, "video")
    
    parts=route.split("/")
    
    cut_filename=DownloadParts.cut_video(foldername, start, end, filename=parts[-1])
    
    route=os.path.join(foldername, cut_filename)
    
    return route




def partial_download(url, start, end):
    
    if "https://" not in url:
        return
    elif "youtube" not in url:
        return
    
    dirname="data"

    
    if ("@" in url) or ("channel" in url):
        return -1, -1
    elif "playlist" in url:
        return -1, -1
    
    
    try:
        foldername = os.path.join(dirname, "video")
        filename, title=DownloadParts.video_download(url, foldername)
        
            
        cut_filename=DownloadParts.cut_video(foldername, start, end, filename=filename)
        
        # 이전파일 삭제
        prev_route=os.path.join(foldername, filename)
        if os.path.isfile(prev_route):
            os.remove(prev_route)
        
        route=os.path.join(foldername, cut_filename)
            
        return route, title
    except:
        return -1, -1




def playlist_urls(url):
    try:
        urls=DownloadParts.get_playlist(url)
        return urls
    except:
        return -1


# url ="https://www.youtube.com/watch?v=4HjcypoChfQ"

# partial_download(url, "00:00:01", "00:01:07")