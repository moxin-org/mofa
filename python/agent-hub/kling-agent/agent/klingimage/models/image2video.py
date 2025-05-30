"""
Models for the Kling AI Image-to-Video API.

This module contains Pydantic models that represent the request and
response data structures for the Kling AI API, specifically for the
image-to-video generation functionality.
"""
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, field_validator


class TaskStatus(str, Enum):
    """Enum representing possible states of a Kling API task."""
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    SUCCEED = "succeed"
    FAILED = "failed"


class TrajectoryPoint(BaseModel):
    """A 2D point representing a position in a trajectory."""
    x: int = Field(..., description="X coordinate (horizontal)")
    y: int = Field(..., description="Y coordinate (vertical)")


class DynamicMask(BaseModel):
    """Configuration for a dynamic mask used to control motion in specific areas."""
    mask: str = Field(..., description="URL or Base64 encoded image of the mask")
    trajectories: List[TrajectoryPoint] = Field(
        ..., 
        description="Sequence of points defining the motion trajectory",
        min_items=2,  # At least 2 points needed for a trajectory
        max_items=77  # Maximum points allowed per docs
    )


class CameraControlConfig(BaseModel):
    """Configuration parameters for camera movement in generated videos."""
    horizontal: float = Field(0, description="Horizontal camera movement", ge=-10, le=10)
    vertical: float = Field(0, description="Vertical camera movement", ge=-10, le=10)
    pan: float = Field(0, description="Horizontal rotation (around Y axis)", ge=-10, le=10)
    tilt: float = Field(0, description="Vertical rotation (around X axis)", ge=-10, le=10)
    roll: float = Field(0, description="Rotation around Z axis", ge=-10, le=10)
    zoom: float = Field(0, description="Zoom level change", ge=-10, le=10)

    @field_validator('*')
    def validate_only_one_non_zero(cls, v, info):
        """
        Ensure that only one of the camera control parameters is non-zero.
        This validator is applied to all fields.
        """
        # Skip validation during initial field validation, only run after all fields populated
        if not hasattr(info.context, 'data'):
            return v
        
        # Only perform the validation on the last field (which is 'zoom')
        if info.field_name == 'zoom':
            data = dict(info.context.data)
            # Check if more than one field has a non-zero value
            non_zero_params = [k for k, val in data.items() if val != 0]
            if len(non_zero_params) > 1:
                raise ValueError("Only one camera control parameter can be non-zero")
            if len(non_zero_params) == 0:
                raise ValueError("At least one camera control parameter must be non-zero")
        return v


class CameraControl(BaseModel):
    """Parameters for controlling camera movement in generated videos."""
    type: Literal["simple", "down_back", "forward_up", "right_turn_forward", "left_turn_forward"]
    config: Optional[CameraControlConfig] = Field(
        None, 
        description="Required when type is 'simple', otherwise should not be provided"
    )

    @field_validator('config')
    def validate_config_based_on_type(cls, v, info):
        """
        Ensure that config is only provided when type is 'simple',
        and required when type is 'simple'.
        """
        if not hasattr(info.context, 'data'):
            return v

        camera_type = info.context.data.get('type')
        if camera_type == 'simple' and v is None:
            raise ValueError("config is required when camera control type is 'simple'")
        
        if camera_type != 'simple' and v is not None:
            raise ValueError("config should not be provided when camera control type is not 'simple'")
        
        return v


class ImageToVideoRequest(BaseModel):
    """Request body for creating an image-to-video generation task."""
    model_name: str = Field(
        default="kling-v1", 
        description="Model name to use for generation",
        pattern="^kling-v[0-9](-[0-9])?$"
    )
    image: Optional[str] = Field(
        None,
        description="Base64 encoded image or URL to an image file"
    )
    image_tail: Optional[str] = Field(
        None,
        description="Base64 encoded image or URL to an image that will be the last frame"
    )
    prompt: Optional[str] = Field(
        None,
        description="Text description of the desired video content",
        max_length=2500
    )
    negative_prompt: Optional[str] = Field(
        None,
        description="Text description of content to avoid in the video",
        max_length=2500
    )
    cfg_scale: float = Field(
        default=0.5,
        description="Generation freedom factor (higher means more adherence to prompt)",
        ge=0,
        le=1
    )
    mode: Literal["std", "pro"] = Field(
        default="std",
        description="Generation mode - standard or professional quality"
    )
    static_mask: Optional[str] = Field(
        None,
        description="Base64 encoded mask image or URL to mask defining static areas"
    )
    dynamic_masks: Optional[List[DynamicMask]] = Field(
        None,
        description="List of dynamic mask configurations",
        max_items=6
    )
    camera_control: Optional[CameraControl] = Field(
        None,
        description="Camera movement configuration"
    )
    duration: Literal["5", "10"] = Field(
        default="5",
        description="Duration of the generated video in seconds"
    )
    callback_url: Optional[HttpUrl] = Field(
        None,
        description="URL to receive task status updates"
    )
    external_task_id: Optional[str] = Field(
        None,
        description="Client-defined task identifier"
    )

    @field_validator('image', 'image_tail')
    def validate_at_least_one_image(cls, v, info):
        """Ensure that at least one of image or image_tail is provided."""
        if not hasattr(info.context, 'data'):
            return v
        
        # Only validate when checking image_tail to avoid duplicate validation
        if info.field_name == 'image_tail':
            image = info.context.data.get('image')
            if image is None and v is None:
                raise ValueError("At least one of 'image' or 'image_tail' must be provided")
        
        return v

    @field_validator('duration')
    def validate_duration_with_features(cls, v, info):
        """Validate duration constraints based on other parameters."""
        if not hasattr(info.context, 'data'):
            return v
        
        # Check if we're using features that only support 5s duration
        data = info.context.data
        has_image_tail = data.get('image_tail') is not None
        has_masks = data.get('static_mask') is not None or data.get('dynamic_masks') is not None
        
        if (has_image_tail or has_masks) and v != "5":
            raise ValueError(
                "When using image_tail, static_mask, or dynamic_masks, duration must be '5'"
            )
        
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model_name": "kling-v1",
                    "mode": "pro",
                    "duration": "5",
                    "image": "https://example.com/sample-image.jpg",
                    "prompt": "Astronaut standing up and walking away",
                    "cfg_scale": 0.5
                }
            ]
        }
    }


class VideoResult(BaseModel):
    """Information about a generated video."""
    id: str = Field(..., description="Unique identifier for this video")
    url: HttpUrl = Field(..., description="URL where the video can be accessed")
    duration: str = Field(..., description="Duration of the video in seconds")


class TaskResult(BaseModel):
    """Task result containing generated videos."""
    videos: Optional[List[VideoResult]] = Field(
        None, 
        description="List of generated videos (only available when task is completed)"
    )


class TaskInfo(BaseModel):
    """Information about a task."""
    external_task_id: Optional[str] = Field(
        None, 
        description="Client-defined task identifier"
    )


class ImageToVideoResponse(BaseModel):
    """Response from creating or retrieving an image-to-video task."""
    code: int = Field(..., description="Response code, 0 means success")
    message: str = Field(..., description="Response message")
    request_id: str = Field(..., description="Unique request identifier")
    data: Union[Dict, List[Dict]] = Field(..., description="Response data")


class TaskResponseData(BaseModel):
    """Data returned from a task creation or status check."""
    task_id: str = Field(..., description="Unique task identifier")
    task_status: TaskStatus = Field(..., description="Current status of the task")
    task_status_msg: Optional[str] = Field(None, description="Additional status details")
    task_info: TaskInfo = Field(..., description="Task information")
    task_result: Optional[TaskResult] = Field(None, description="Task results (when successful)")
    created_at: int = Field(..., description="Task creation timestamp (Unix ms)")
    updated_at: int = Field(..., description="Task last updated timestamp (Unix ms)")