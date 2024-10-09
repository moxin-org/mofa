# Moly client integration example

This is a quick example to showcase how use the `dora-openai-server` to receive and send back data.

Dora Openai Server is still experimental and may change in the future.

```bash
dora up
dora build dataflow.yml
dora start dataflow.yml

# In a separate terminal
python moly_client_simulation.py
```

The `moly_client_simulation` script is simulating input from Moly. The `Chat Completion Response` will be sent to Moly while the actual moly interface is ready. 

