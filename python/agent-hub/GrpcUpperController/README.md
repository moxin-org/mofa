# grpc_upper_controller

Test and relay gRPC navigation service connectivity for Dora-Mofa using UpperController proto.

## Features
- Stateless agent to connect and test gRPC robotic navigation services
- Relays common endpoint results (`sendEndAction`, `recvEndState`, `setConfig`, `getConfig`)
- Receives user triggering input for composability in Dora/Mofa pipelines

## Getting Started

### Installation
Install via cargo:
```bash
pip install -e .
```

## Basic Usage

Create a YAML config (e.g., `demo.yml`):

```yaml
nodes:
  - id: grpc_upper_controller
    build: pip install -e grpc_upper_controller
    path: grpc_upper_controller
    inputs:
      user_input: input/user_input
    outputs:
      - grpc_test_result
    env:
      GRPC_SERVER_ADDRESS: "localhost"
      GRPC_SERVER_PORT: "50051"
```

Run the demo:

```bash
dora build demo.yml
dora start demo.yml
```


## Integration with Other Nodes

To connect with your existing node:

```yaml
nodes:
  - id: upstream
    build: pip install my-upstream
    path: my-upstream
    outputs:
      - user_input
  - id: grpc_upper_controller
    build: pip install -e grpc_upper_controller
    path: grpc_upper_controller
    inputs:
      user_input: upstream/user_input
    outputs:
      - grpc_test_result
```

Your point source must output:

* Topic: `user_input`
* Data: Any object (could be None)
* Metadata:

  ```json
  {
    "description": "Dummy/trigger input (can be None, used to trigger calls)"
  }
  ```

## API Reference

### Input Topics

| Topic         | Type      | Description                                         |
| -------------| --------- | --------------------------------------------------- |
| user_input    | Any       | Dummy/trigger input (optional; triggers test calls)  |

### Output Topics

| Topic             | Type                | Description                         |
| ---------------- | ------------------- | ----------------------------------- |
| grpc_test_result  | Dict / str (JSON)   | JSON dict of endpoint test results  |


## License

Released under the MIT License.
