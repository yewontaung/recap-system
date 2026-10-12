from pathlib import Path
import tempfile
import uuid

from aiogram.types import Message, Video


async def upload_via_telegram(video:Video, message:Message) -> str:
    if video.file_size and video.file_size > 20 * 1024 * 1024:
        raise ValueError("Video is too large.")
    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = Path(temp_dir) / f"{uuid.uuid4()}.mp4"
        await message.bot.download(video, destination=video_path)
        return video_path