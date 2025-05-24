# Euterpe Examples

This directory contains example scripts demonstrating how to use the Euterpe library.

## Minimal Example

The `minimal_example.py` script shows the bare minimum code needed to generate a video with Euterpe. This is a great starting point if you're new to the library.

```bash
python minimal_example.py
```

## Simple Video Generation Example

The `simple_video_generation.py` script demonstrates how to use the core functionality of Euterpe to generate a video from keyframes with music, with more configuration options and features.

### Prerequisites

- Euterpe package installed (`pip install -e ..` from this directory)
- API keys set in environment variables (or added to the script for testing)
  - `KLING_API_KEY` - for image generation 
  - `BEATOVEN_API_KEY` - for music generation
  - `DIFY_API_KEY` - optional, for prompt enhancement

### Running the Example

Basic usage:

```bash
python simple_video_generation.py
```

Custom options:

```bash
python simple_video_generation.py --output my_video --output-dir ./custom_output --enhance
```

Available options:
- `--output`: Base name for output files (default: "mountain_journey")
- `--enhance`: Enable prompt enhancement with Dify (default: disabled)
- `--output-dir`: Directory to save generated files (default: "./euterpe_output")
- `--show-vendor-info`: Display information about integrated vendor modules

### Understanding the Code

The example demonstrates:
1. Setting up the environment and API keys
2. Creating keyframes with prompts
3. Configuring image generation parameters
4. Configuring music generation
5. Creating a video generation request
6. Handling the results

This serves as a template you can modify for your own projects.

## Custom Workflow Example

The `custom_workflow_example.py` script shows how to work with Euterpe's internal components directly for more advanced use cases.

## Notes on Vendor Integration

Euterpe now integrates BeatovenDemo and KlingDemo directly as vendor modules within the package. This eliminates the need to install these dependencies separately. 

You can run the simple example with the `--show-vendor-info` flag to see details:

```bash
python simple_video_generation.py --show-vendor-info
```
