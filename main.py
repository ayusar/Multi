import os,json,threading,subprocess
from flask import Flask
app=Flask(__name__)
@app.route('/'):lambda:"OK"

def run(repo,cmd,env_vars):
    name=repo.split('/')[-1].replace('.git','')
    if not os.path.exists(name):subprocess.run(f"git clone {repo} {name}",shell=True)
    os.chdir(name)
    env={**os.environ,**env_vars}
    subprocess.run(cmd,shell=True,env=env)

config=json.loads(os.environ.get('BOTS_CONFIG','{}'))
for repo,data in config.items():
    threading.Thread(target=run,args=(repo,data['cmd'],data.get('env',{}))).start()
app.run(host='0.0.0.0',port=int(os.environ.get('PORT',8000)))
