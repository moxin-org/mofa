
### 1. Install the MAE Project
Refer to the [install_mae](install_mae_en.md) document to install the MAE project.
Due to issues with dynamic-node in dora-rs version 3.5, we are using dora(v0.3.6-rc0) to run this program. The installation steps are as follows:

```bash
sudo rm $(which dora)
pip uninstall dora-rs

## Install dora binary
git clone https://github.com/dora-rs/dora.git
cd dora
cargo build --release -p dora-cli
PATH=$PATH:$(pwd)/target/release

## Install Python API
maturin develop -m apis/python/node/Cargo.toml

dora --help
```


### 2. Configure Agent Parameters
In the `Moxin-App-Engine/mae/agent-applications` directory, you will find all currently available agents, with more being added regularly. You need to configure the YAML files located under `configs` for each agent, especially the API configurations. You can also set it up to use the Ollama model.

**For OpenAI**:
```yaml
MODEL:
  MODEL_API_KEY:  
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
```

**For Ollama**:
```yaml
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
```

### 3. Activate Agents via Command Line

#### 3.1 Various Command Line Options

**List Available Agents**:
```shell
mofa agent-list
```

**Run an Agent**:
```shell
mofa run --agent-name reasoner
```

**How to Stop an Agent**:
Simply type `exit` or `quit` in the command line to stop the agent.

### Q: What Should I Do If Dora Freezes?
**A:** It’s recommended to use the following command with `sudo`:
```shell
pkill dora
```
*Note: This will terminate all processes related to "dora," so use it with caution.*

---