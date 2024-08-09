import os

from fastapi import FastAPI,HTTPException,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from mae.run.run_dataflow import run_dora_dataflow
from mae.server.item_request import AgentDataflow, AgentNodeConfig, RunAgent, UploadAgentNodeConfig, UploadFiles
from mae.server.process import load_node_config, upload_node_config
from mae.server.util import get_agent_list, load_agent_dataflow
from mae.agent_link.agent_template import  agent_template_path
from mae.utils.files.dir import make_dir

app = FastAPI()

# config cors policy, allow incoming request from localhost:5173 (dev frontend)
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get("/agent_list",summary="get agent list")
def agent_list():
    try:
        agent_list = get_agent_list()
        return JSONResponse(status_code=200, content={'status':'success','data':agent_list})
    except Exception as e :
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})

@app.post("/agent_dataflow",summary="load agent dora dataflow ")
def agent_dataflow(item:AgentDataflow):
    agent_name = item.agent_name.lower()
    try:
        agent_dataflow = load_agent_dataflow(agent_name=agent_name)
        return JSONResponse(status_code=200, content={'status':'success','data':agent_dataflow})
    except Exception as e :
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})

@app.post("/agent_node_config",summary="get agent dataflow node config")
def agent_node_config(item:AgentNodeConfig):
    agent_name = item.agent_name.lower()
    node_id = item.node_id.lower()
    try:
        agent_dataflow = load_node_config(agent_name=agent_name,node_id=node_id)
        return JSONResponse(status_code=200, content={'status':'success','data':agent_dataflow})
    except Exception as e :
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})

@app.post("/run_agent",summary="use dora run agent dataflow ")
def run_agent(item:RunAgent):
    try:
        if item.work_dir is None or item.work_dir=='string':
            item.work_dir = agent_template_path
        agent_result = run_dora_dataflow(work_dir=item.work_dir,task_input=item.task_input,
                          is_load_node_log=item.is_load_node_log,dataflow_name=item.agent_name,
                          agent_name=item.agent_name)
        return JSONResponse(status_code=200, content={'status':'success','data':agent_result})
    except Exception as e:
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})

@app.post("/upload_agent_node_config",summary="upload dataflow node config")
def upload_agent_node_config(item:UploadAgentNodeConfig):
    try:
        agent_result = upload_node_config(agent_name=item.agent_name,node_id=item.node_id,node_config=item.node_config)
        return JSONResponse(status_code=200, content={'status':'success','data':agent_result})
    except Exception as e:
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})


@app.post("/upload_files/",summary="upload dataflow node config")
async def upload_files(item:UploadFiles):
    try:

        upload_file_dir_path = agent_template_path +f'/{item.agent_name}/data/inputs'
        make_dir(dir_path=upload_file_dir_path)
        saved_files = []
        for file in item.files:
            file_location = os.path.join(upload_file_dir_path, file.filename)
            with open(file_location, "wb") as f:
                while True:
                    chunk = await file.read(2048)  # 每次读取1024字节
                    if not chunk:
                        break
                    f.write(chunk)
            saved_files.append(os.path.join(upload_file_dir_path, file.filename))
        return JSONResponse(status_code=200, content={'status': 'success', 'data': saved_files})
    except Exception as e:
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)