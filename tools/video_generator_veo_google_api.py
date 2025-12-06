import logging
from typing import List
import asyncio
from google import genai
from google.genai import types
from interfaces.video_output import VideoOutput

# https://ai.google.dev/gemini-api/docs/video-generation?hl=zh-cn


class VideoGeneratorVeoGoogleAPI:
    def __init__(
        self,
        api_key: str,
        t2v_model: str = "veo-3.1-generate-preview",
        ff2v_model: str = "veo-3.1-generate-preview",
        flf2v_model: str = "veo-3.1-generate-preview",
    ):
        self.api_key = api_key
        self.t2v_model = t2v_model
        self.ff2v_model = ff2v_model
        self.flf2v_model = flf2v_model

        self.client = genai.Client(
            api_key=api_key,
        )
    
    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: List[str],
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        duration: int = 8,
    ) -> VideoOutput:

        params = {
            "prompt": prompt,
        }
        config_params = {
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "duration_seconds": duration,
        }
        if len(reference_image_paths) == 0:
            params["model"] = self.t2v_model
        elif len(reference_image_paths) == 1:
            params["model"] = self.ff2v_model
            params["image"] = types.Image.from_file(location=reference_image_paths[0])
        elif len(reference_image_paths) == 2:
            params["model"] = self.flf2v_model
            params["image"] = types.Image.from_file(location=reference_image_paths[0])
            config_params["last_frame"] = types.Image.from_file(location=reference_image_paths[1])
        else:
            raise ValueError("The number of reference images must be no more than 2")

        logging.info(f"Calling {params['model']} to generate video...")

        operation = self.client.models.generate_videos(
            **params,
            config=types.GenerateVideosConfig(**config_params),
        )

        while not operation.done:
            await asyncio.sleep(2)
            operation = self.client.operations.get(operation)
            logging.info(f"Video generation not completed, waiting 2 seconds...")

        # 检查 API 响应是否有效
        if operation.response is None:
            error_msg = f"视频生成失败：API 返回空响应。操作详情: {operation}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
        
        if operation.response.generated_videos is None or len(operation.response.generated_videos) == 0:
            # 尝试获取更多错误信息
            error_details = getattr(operation, 'error', None)
            error_msg = f"视频生成失败：没有生成任何视频。"
            if error_details:
                error_msg += f" 错误详情: {error_details}"
            error_msg += f" 完整响应: {operation.response}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video)

        video_output = VideoOutput(
            fmt="bytes",
            ext="mp4",
            data=generated_video.video.video_bytes,
        )
        return video_output
