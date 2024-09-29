# Configuration Schema for Agents, Composite Agents, and Libraries

This document describes the YAML schema used to configure agents, composite agents, and libraries.

## Schema Overview

The schema supports three types of configurations:
- `agent`
- `compositeAgent`
- `library`

Each configuration type has specific properties and structure.

## Common Properties

All configuration types share the following common properties:

- `name` (string, required): The name of the configuration.
- `type` (string, required): The type of the configuration. Must be one of `agent`, `compositeAgent`, or `library`.
- `version` (string, required): The version of the configuration.
- `description` (string, required): A description of the configuration.

## Agent Configuration

An `agent` configuration defines a single agent with the following properties:

- `inputs` (array of objects, optional): Defines the inputs for the agent.
  - `name` (string, required): The name of the input.
  - `connecto` (string, required): The connection string for the input.
- `outputs` (array of objects, optional): Defines the outputs for the agent.
  - `name` (string, required): The name of the output.
  - `formats` (array of strings, optional): The formats supported by the output.
- `source` (object, required): Defines the source files for the agent.
  - `python` (string, required): The Python source file.
  - `xlang` (string, required): The XLang source file.
  - `shared_lib` (string, required): The shared library file.
- `parameters` (object, required): Defines the parameters for the agent.
  - Additional properties are allowed.
- `group` (string, optional): The execution group for the agent.

## Composite Agent Configuration

A `compositeAgent` configuration defines a composite agent that orchestrates multiple agents. It includes the following properties:

- `imports` (array of objects, optional): Defines the files to import.
  - `file` (string, required): The file to import.
  - `alias` (string, required): The alias for the imported file.
- `agents` (array of objects, required): Defines the agents within the composite agent.
  - See the Agent Configuration section for the structure of each agent.
- `connections` (array of objects, required): Defines the connections between agents.
  - `fromNodeName` (string, required): The name of the source agent.
  - `fromPinName` (string, required): The name of the source pin.
  - `toNodeName` (string, required): The name of the destination agent.
  - `toPinName` (string, required): The name of the destination pin.
- `groups` (array of objects, optional): Defines the execution groups for the agents.
  - `name` (string, required): The name of the group.
  - `agents` (array of strings, required): The agents in the group.

## Library Configuration

A `library` configuration defines a collection of agents. It includes the following properties:

- `agents` (array of objects, required): Defines the agents within the library.
  - See the Agent Configuration section for the structure of each agent.

