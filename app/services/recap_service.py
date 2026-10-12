import asyncio
from pathlib import Path
import re

from google import genai
from sqlmodel import Session, select

from app.database.models import AIApiKey, Account
from app.utils.enums import ClientType


async def generate_recap(video_path:str, user_id:str, client:ClientType, session:Session):
    match client:
        case ClientType.TELEGRAM: return await _generate_recap_via_telegram(video_path, user_id, session)
    return

async def _generate_recap_via_telegram(video_path:str, user_id:str, session:Session):

    account = session.exec(select(Account).where(Account.reference_id == user_id)).one_or_none()
    
    if not account:
        raise ValueError(f"Account not found.")
    
    api_key = session.exec(select(AIApiKey).where(AIApiKey.account_id == account.account_id)).one_or_none()
    
    if not api_key:
        raise ValueError(f"API not found.")

    return await analyze_video(video_path, api_key.hashed_key)


async def analyze_video(video_path:str, api_key:str):

    path = Path(video_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Video file not found: {path}")

    client = genai.Client(api_key=api_key)

    try:
        video_file = await asyncio.to_thread(client.files.upload, file=str(path))
        while True:
            state = video_file.state
            if state and state.name == "ACTIVE":
                break
            if state and state.name == "FAILED":
                raise RuntimeError("Gemini failed to process the video.")

            await asyncio.sleep(5)

            video_file = await asyncio.to_thread(client.files.get, name=video_file.name)
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.5-flash",
                contents=[
                    video_file,
                    """
                    Create an SRT file containing a Burmese recap of the video.
                    Requirements:
                    - use natural, readable Burmese,
                    -
                    - use this exact SRT format:
                        1 00:00:00,000 --> Text
                        2 00:00:04,000 --> Text
                    """
                ]
            )

            srt_text = (response.text or "").strip()
            srt_text = re.sub(r"^```(?:srt|text)?\s*|\s*```$", "", srt_text, flags=re.IGNORECASE)

            output_path = Path(video_path).with_suffix(".srt")
            output_path.write_text(srt_text + "\n", encoding="utf-8")
            
            return output_path

    finally:
        pass
