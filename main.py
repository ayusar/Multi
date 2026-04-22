import os,json,subprocess,threading,time,urllib.request
from flask import Flask

app=Flask(__name__)
@app.route('/')
def home():
    return """<center><img src='https://i.giphy.com/media/3o7abAHdYvZdBNnGZq/giphy.webp' style='border-radius:12px'/><style>body{background:antiquewhite}</style></center>"""

def ping():
    while True:
        try:urllib.request.urlopen("http://0.0.0.0:8080",timeout=5)
        except:pass
        time.sleep(120)

def setup_bot(name,cfg):
    if not os.path.exists(name):
        subprocess.run(f"git clone {cfg['source']} {name}",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    req=f"{name}/requirements.txt"
    if os.path.exists(req):
        subprocess.run(f"pip install -q -r {req}",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def run_bot(name,cfg):
    while True:
        setup_bot(name,cfg)
        env={**os.environ,**cfg.get('env',{})}
        script=cfg.get('run','main.py')
        print(f"[{name}] Running {script}")
        proc=subprocess.Popen(["python",f"{name}/{script}"],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        proc.wait()
        print(f"[{name}] Crashed! Restarting in 5s...")
        time.sleep(5)

if __name__=="__main__":
    with open("config.json") as f:
        bots=json.load(f)
    
    threading.Thread(target=ping,daemon=True).start()
    
    for name,cfg in bots.items():
        if not cfg.get('source','').startswith('https://github.com/<'):
            threading.Thread(target=run_bot,args=(name,cfg),daemon=True).start()
            time.sleep(2)
    
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8080)))
