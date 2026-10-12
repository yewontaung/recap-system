import tempfile

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.database import get_session
from app.database.models import Account
from app.dtos.inputs.api_key_form import APIKeyForm
from app.dtos.inputs.create_account_form import CreateAccountForm
from app.services import account_service, api_key_service, recap_service, video_service
from app.utils.enums import ClientType


router = Router()

class AccountSetupState(StatesGroup):
    waiting_for_api_key = State()

@router.message(CommandStart())
async def handle_start(message:Message, state: FSMContext):
    user = message.from_user
    
    if user is None or user.is_bot:
        return

    form = CreateAccountForm(
        reference_id=str(user.id),
        username=user.username or user.id,
        fullname=user.full_name or user.first_name or user.username or "anonymous",
    )


    with get_session() as session:
        try:
            account_service.create_from_resource(form, policy=Account.SignUpPolicy.TELEGRAM, session=session)
            await state.set_state(AccountSetupState.waiting_for_api_key)
        except Exception as e:
            if not api_key_service.has_api_key_by_user_id(user.id, ClientType.TELEGRAM, session):
                await message.answer(f"Please enter your gemini api key to start using the bot.")
                await state.set_state(AccountSetupState.waiting_for_api_key)

            return
    
    await message.answer("Welcome to the Recap System Bot!\nPlease enter gemini api key to start using the bot.")

@router.message(AccountSetupState.waiting_for_api_key)
async def handle_receive_api_key(message:Message, state:FSMContext):
    api_key = message.text.strip()

    form = APIKeyForm(api_key=api_key)
    with get_session() as session:
        api_key_service.add_api_key(form, client=ClientType.TELEGRAM, user_id=str(message.from_user.id), session=session)

    await state.clear()
    await message.answer("Thank you! Your API key has been received and your account is now set up.")

@router.message(F.video)
async def handle_video(message:Message):
    await message.answer("Video received! Processing your video...")
    video = message.video
    if not video:
        await message.answer("No video found in the message.")
        return

    try:
        with get_session() as session:
            with tempfile.TemporaryDirectory() as temp_dir:
                uploaded_path = await video_service.upload_via_telegram(video, temp_dir, message)
                result = await recap_service.generate_recap(uploaded_path, str(message.from_user.id), ClientType.TELEGRAM, session)
                await message.answer_document(FSInputFile(result, filename="recap.srt"))
                
    except Exception as e:
        await message.answer(str(e))
