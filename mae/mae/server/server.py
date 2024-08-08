from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from mae.run.run_dataflow import run_dora_dataflow
from mae.server.item_request import AgentDataflow, AgentNodeConfig, RunAgent
from mae.server.process import load_node_config
from mae.server.util import get_agent_list, load_agent_dataflow
from mae.agent_link.agent_template import  agent_template_path

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
        # result = dora_run_agent(item.inputs)
        agent_result = run_dora_dataflow(work_dir=item.work_dir,task_input=item.task_input,
                          is_load_node_log=item.is_load_node_log,dataflow_name=item.agent_name,
                          agent_name=item.agent_name)
        return JSONResponse(status_code=200, content={'status':'success','data':agent_result})
    except Exception as e:
        return JSONResponse(status_code=404, content={'status':'error','message':str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)