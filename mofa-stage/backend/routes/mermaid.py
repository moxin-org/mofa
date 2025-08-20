from flask import Blueprint, request, jsonify, current_app
import os, sys, yaml, json, requests

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DEFAULT_MOFA_MODE
from routes.settings import get_settings

mermaid_bp = Blueprint('mermaid', __name__, url_prefix='/api/mermaid')

def yaml_to_mermaid(yaml_str: str):
    """Convert MoFA dataflow YAML (two possible schemas) to Mermaid flowchart code"""
    try:
        data = yaml.safe_load(yaml_str)

        nodes: set[str] = set()
        edge_tuples: list[tuple[str, str, str]] = []  # (src, dst, label)

        def add_edge(src: str, dst: str, label: str = ""):
            if src and dst and src != dst:
                edge_tuples.append((src, dst, label))

        # Schema 1: { step_name: { inputs: {...} } }
        if isinstance(data, dict) and 'nodes' not in data:
            for step, cfg in data.items():
                nodes.add(step)
                if not isinstance(cfg, dict):
                    continue
                inputs = cfg.get('inputs', {})

                if isinstance(inputs, dict):
                    for label, upstream in inputs.items():
                        if isinstance(upstream, str):
                            src = upstream.split('/')[0]
                            add_edge(src, step, label)
                elif isinstance(inputs, list):
                    for upstream in inputs:
                        if isinstance(upstream, str):
                            src = upstream.split('/')[0]
                            add_edge(src, step)

        # Schema 2: top-level key 'nodes' with list items
        if isinstance(data, dict) and isinstance(data.get('nodes'), list):
            for node in data['nodes']:
                if not isinstance(node, dict):
                    continue
                nid = node.get('id') or node.get('name')
                if not nid:
                    continue
                nodes.add(nid)

                inputs = node.get('inputs', {})
                if isinstance(inputs, dict):
                    for label, upstream in inputs.items():
                        if isinstance(upstream, str):
                            src = upstream.split('/')[0]
                            add_edge(src, nid, label)
                elif isinstance(inputs, list):
                    for upstream in inputs:
                        if isinstance(upstream, str):
                            src = upstream.split('/')[0]
                            add_edge(src, nid)

        # Build diagram
        diagram: list[str] = ["flowchart TB"]
        for n in sorted(nodes):
            diagram.append(f"  {n}")

        # deduplicate edges
        seen = set()
        for src, dst, label in edge_tuples:
            key = (src, dst, label)
            if key in seen:
                continue
            seen.add(key)
            if label:
                diagram.append(f"  {src} -- {label} --> {dst}")
            else:
                diagram.append(f"  {src} --> {dst}")

        return "\n".join(diagram)
    except Exception:
        return None

@mermaid_bp.route('/preview', methods=['POST'])
def preview():
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON required"}), 400
    data = request.json
    yaml_code = data.get('yaml', '')
    use_llm = data.get('use_llm', False)
    if not yaml_code:
        return jsonify({"success": False, "message": "yaml empty"}), 400
    # 1. try local conversion
    mermaid_code = yaml_to_mermaid(yaml_code)
    if mermaid_code:
        return jsonify({"success": True, "mermaid": mermaid_code})
    # 2. fallback llm
    if use_llm:
        settings = get_settings()
        api_key = settings.get('gemini_api_key', '')
        if not api_key:
            return jsonify({"success": False, "message": "GEMINI_API_KEY not set"}), 400
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"Convert the following mofa dataflow yaml to a mermaid flowchart code, only output code:\n{yaml_code}"}]}]
        }
        try:
            resp = requests.post(endpoint, json=payload, timeout=20)
            if resp.status_code == 200:
                mermaid = resp.json()['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"success": True, "mermaid": mermaid})
            else:
                return jsonify({"success": False, "message": resp.text}), 500
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    return jsonify({"success": False, "message": "conversion failed"}), 500

@mermaid_bp.route('/export', methods=['POST'])
def export_html():
    """Convert YAML to Mermaid HTML and save next to the YAML file.

    Request JSON:
    {
        "agent": "add_numbers",                # agent name
        "yaml_path": "add_numbers_dataflow.yml", # relative path inside agent dir
        "yaml": "..."                            # raw yaml string (optional if server can read)
    }
    The HTML will be written to same directory with suffix "-graph.html".
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "JSON required"}), 400

    data = request.json
    agent_name = data.get('agent')
    yaml_path = data.get('yaml_path')
    yaml_code = data.get('yaml', '')

    if not agent_name or not yaml_path:
        return jsonify({"success": False, "message": "agent and yaml_path required"}), 400

    # If yaml not provided, attempt to read from disk via MofaCLI
    if not yaml_code:
        from utils.mofa_cli import MofaCLI  # local import to avoid cycle
        mofa_cli = MofaCLI(get_settings())
        read_res = mofa_cli.read_file(agent_name, yaml_path)
        if not read_res.get('success'):
            return jsonify(read_res), 400
        yaml_code = read_res.get('content', '')

    mermaid_code = yaml_to_mermaid(yaml_code)
    if not mermaid_code:
        return jsonify({"success": False, "message": "conversion failed"}), 500

    html = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'></head>"
        "<body><div class='mermaid'>\n" + mermaid_code + "\n</div>"
        "<script src='https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'></script>"
        "<script>mermaid.initialize({ startOnLoad:true, securityLevel:'loose', theme:'base' });</script>"
        "</body></html>"
    )

    # Determine html path: replace .yml/.yaml with -graph.html
    base_name = os.path.basename(yaml_path)
    dir_name = os.path.dirname(yaml_path)
    name_no_ext = os.path.splitext(base_name)[0]
    html_file = name_no_ext + "-graph.html"
    html_path = os.path.join(dir_name, html_file) if dir_name else html_file

    from utils.mofa_cli import MofaCLI
    mofa_cli = MofaCLI(get_settings())
    write_res = mofa_cli.write_file(agent_name, html_path, html)

    if write_res.get('success'):
        return jsonify({"success": True, "html_path": html_path})
    else:
        return jsonify(write_res), 500 