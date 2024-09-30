import json

from dora import Node, DoraStatus
import pyarrow as pa
from mofa.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            config = {}
            params = read_yaml('use_case/summarize_pdf_by_rag_dspy.yml')
            if 'AGENT' in params:
                model_config,agent_config,env_config,rag_config = params['MODEL'],params['AGENT'],params['ENV'],params.get('RAG',None)
                config = {}
                for i in [model_config,agent_config,env_config]:
                    config.update(i)
                if rag_config is not None:
                    config.update(rag_config)
                config = {k.lower(): v for k, v in config.items()}
            else:
                config = params
            if dora_event["type"] == "INPUT":
                send_output("agent_config", pa.array([json.dumps(config)]),dora_event['metadata'])
        return DoraStatus.STOP