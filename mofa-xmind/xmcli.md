---

# xmcli Usage Guide

`xmcli` is a command-line tool designed to interact with the `xMind` platform, specifically for managing key-value pairs in a keystore. Before using `xmcli`, ensure that `xMind` is running.

## Prerequisites

- **xMind**: Ensure that `xMind` is started and running on the appropriate port (`lrpc:99023`).

## Command Syntax

The `xmcli` tool supports three primary operations: updating, retrieving, and deleting keys in the keystore.

### 1. Update a Key

To update or add a key-value pair in the keystore:

```bash
xmcli --updatekey <key_name> <value>
```

or

```bash
xmcli -uk <key_name> <value>
```

#### Example:

```bash
xmcli --updatekey username "admin"
```

This command updates or creates the key `username` with the value `"admin"`.

### 2. Get a Key

To retrieve the value associated with a key from the keystore:

```bash
xmcli --getkey <key_name>
```

or

```bash
xmcli -gk <key_name>
```

#### Example:

```bash
xmcli --getkey username
```

This command retrieves the value associated with the key `username`.

### 3. Delete a Key

To delete a key-value pair from the keystore:

```bash
xmcli --deletekey <key_name>
```

or

```bash
xmcli -dk <key_name>
```

#### Example:

```bash
xmcli --deletekey username
```

This command deletes the key `username` from the keystore.

## Handling Errors

- If the key does not exist when retrieving or deleting, `xmcli` will output a message indicating the absence of the key.
- If the command is not used with the correct number of arguments, the usage guide will be displayed.

## Common Issues

- **xMind Not Running**: Ensure that `xMind` is started before using `xmcli`. The tool connects to `xMind` through `lrpc:99023`.
- **Incorrect Command Usage**: Make sure to use the correct syntax for each operation.

## Examples

- **Updating a Key**:
  
  ```bash
  xmcli -uk apiKey "12345-abcde"
  ```

- **Retrieving a Key**:
  
  ```bash
  xmcli -gk apiKey
  ```

- **Deleting a Key**:
  
  ```bash
  xmcli -dk apiKey
  ```
