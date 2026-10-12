from pathlib import Path

from aiogram.types import Message, Video


async def upload_via_telegram(video:Video, temp_dir:str, message:Message) -> str:
    if video.file_size and video.file_size > 20 * 1024 * 1024:
        raise ValueError("Video is too large.")
    video_path = Path(temp_dir) / "input.mp4"
    await message.bot.download(video, destination=video_path)
    return video_path