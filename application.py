from flask import Flask, render_template, request, send_file
import os
import VideoDownload
import json

app = Flask(__name__)


path_cache=[]



@app.route("/", methods=["GET", "POST"])
def index():
    url1 = request.args.get("url1")
    url2 = request.args.get("url2")
    
    
    if path_cache!=[]:
        for p in path_cache:
            if os.path.isfile(p):
                os.remove(p)
    
    
    
    if url1==None and url2==None:
        return render_template("html/index.html")
    if url1=="" or url2=="":
        return render_template("html/index.html")
    

    if url1 != None:
        if "https://" not in url1:
            return render_template("html/index.html")
            
        if "/playlist?list=" in url1:
            results=VideoDownload.playlist_urls(url1)
            if results==-1:
                return render_template("html/index.html")
            return render_template("html/index.html", datas = results)
        
        
        else:
            
            path, title=VideoDownload.download(url1)
            
            if path==-1:
                return render_template("html/index.html")
            
            path_cache.append(path)
            result={}
            result["path"]=path; result["title"]=title
            
            
            return render_template("html/download.html", data=result)
            
    
    if url2 != None:
        if "https://" not in url2:
            return render_template("html/index.html")
        
        
        start=request.args.get("start")
        end=request.args.get("end")

        path, title=VideoDownload.partial_download(url2, start, end)
        if path==-1:
            return render_template("html/index.html")
        
        path_cache.append(path)
        result={}
        result["path"]=path; result["title"]=title
        
        return render_template("html/download.html", data=result)
    




@app.route("/downloads", methods=["POST"])
def downloads():
    raw_data = request.form.getlist("vids")
    
    videos=[]
    for data in raw_data:
        json_accepted=data.replace("'","\"")
        videos.append(json.loads(json_accepted))
    
    for video in videos:
        route, _=VideoDownload.download(video["url"])
        if route==-1:
            return render_template("html/index.html")
        video["path"]=route
        path_cache.append(route)
        
        
    return render_template("html/downloads.html", datas=videos)





@app.route("/getvid", methods=["POST"])
def get_vid():
    path= request.form.get("videopath")
    return send_file(path, as_attachment=True)
    




if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0')
    
    
    
    
    