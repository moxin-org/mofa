
---

# Object Detection

## 1. Overview

This agent is to showcase how to process images. It is designed to do object detection on a uploaded image, then show the object detection results. 

## 2. Use Cases

## 3. Configuration
In the `object_detection_dataflow.yml` file, please make sure the `terminal-input` points to the right path of your MoFA `node-hub/terminal-input` directory. 
```
- id: terminal-input
    build: pip install -e ../../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
```

## 4. Running

Using Dora-rs Commands

1. Install the MoFA project package
2. Run the following commands：
   ```bash
   dora up && dora build object_detection_dataflow.yml && dora start object_detection_dataflow.yml --attach
   ```
3. Open another terminal and run multiple-terminal-input. Enter the local image file name. 
```
$ terminal-input
 Send You Task :  cat_and_dog.jpg
 Send You Task :  test_image.jpg
 Send You Task :
```

