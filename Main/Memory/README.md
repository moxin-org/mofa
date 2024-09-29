# Memory Folder

The `Memory` folder is designed to store and manage the history of interactions with the language model (LLM). This folder helps in maintaining context and continuity across multiple sessions, enabling the LLM to provide more accurate and context-aware responses.

## Structure

The `Memory` folder typically contains the following files:

- `history.yml`: A YAML file that logs the interactions with the LLM, including user inputs and LLM responses.
- `metadata.json`: A JSON file that stores metadata about the interactions, such as timestamps, session IDs, and user information.
- `README.md`: This file, which provides an overview of the `Memory` folder and its purpose.

## Usage

### Logging Interactions

Each interaction with the LLM is logged in the `history.yml` file. The structure of the log entries is as follows:
