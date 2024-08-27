import json
from aiogram import Dispatcher, types, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


with open('questions.json', 'r') as f:
    questions = json.load(f)

#print(questions_data)

user_data = {}

class TestState(StatesGroup):
    question = State()
    score = State()
    finished = State()


router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer('Добро подаловать в тг-бот на определения уровня твоего английского языка. Тест содержит 100 вопросов и может занять до 20 минут твоего времени. Запостись терпением  и введи /test для начала.')


@router.message(Command('test'))
async def start_test(message: Message, state: FSMContext):
    await state.set_state(TestState.question)
    await state.update_data(score=0, current_question=0)
    await ask_question(message, state)


async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    current_question = data["current_question"]

    if current_question < len(questions):
        question_data = questions[current_question]
        buttons = [KeyboardButton(text=option.strip()) for option in question_data["options"]]

        # Создаем клавиатуру и добавляем кнопки
        keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

        await message.answer(question_data["question"], reply_markup=keyboard)
    else:
        await state.set_state(TestState.score)
        await show_results(message, state)

# Обработка ответа пользователя
@router.message(TestState.question)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    current_question = data["current_question"]
    question_data = questions[current_question]
    if message.text.strip() not in [option.strip() for option in question_data["options"]]:
        await message.answer("Что-то вы не то сделали, попробуйте еще раз ответить, используя клавиатуру ниже.")
        return
    if message.text == question_data["correct"].strip():
        data["score"] += 1

    data["current_question"] += 1
    await state.update_data(score=data["score"], current_question=data["current_question"])
    await ask_question(message, state)


# Показ результатов
async def show_results(message: Message, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    percentage = (score / len(questions)) * 100

    if score >= 85:
        level = "C2"
    elif score >= 68:
        level = "C1"
    elif score >= 51:
        level = "B2"
    elif score >= 34:
        level = "B1"
    elif score >= 17:
        level = "A2"
    else:
        level = "A1"

    await message.answer(f"Ваш результат: {score} из {len(questions)}.\nВаш уровень: {level}, процент побед: {percentage}")
    await state.set_state(TestState.finished)
