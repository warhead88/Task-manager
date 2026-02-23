from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.future import select

from src.db import get_session
from src.tables import Task, User
from src.utils import calculate_initial_remind_time

router = Router()

class RemindForm(StatesGroup):
    waiting_for_task_number = State()
    waiting_for_recurrence = State()
    waiting_for_time = State()

@router.message(Command("remind"))
async def remind_start(message: types.Message, state: FSMContext):
    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()
        if not tasks:
            await message.answer("☕️ У тебя пока нет задач. Добавь их через /add.")
            return

        text = "⏰ *Настройка напоминания*\n\nТвои задачи:\n" + "\n".join(
            f"{i}. {task.description}" for i, task in enumerate(tasks, start=1)
        )
        await message.answer(text + "\n\nНапиши номер задачи, для которой хочешь включить напоминание\n(или 'отмена'):", parse_mode="Markdown")
        await state.set_state(RemindForm.waiting_for_task_number)

@router.message(RemindForm.waiting_for_task_number)
async def process_task_number(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("❌ Настройка напоминания отменена.")
        return

    try:
        index = int(message.text) - 1
    except ValueError:
        await message.answer("⚠️ Введи просто число (номер задачи).")
        return

    async with get_session() as session:
        result = await session.execute(
            select(Task)
            .filter(Task.user_id == message.from_user.id)
            .order_by(Task.id)
        )
        tasks = result.scalars().all()
        if 0 <= index < len(tasks):
            task_id = tasks[index].id
            await state.update_data(task_id=task_id)
            
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Единожды", callback_data="rec_none")],
                [InlineKeyboardButton(text="Каждый день", callback_data="rec_daily")],
                [InlineKeyboardButton(text="По будням", callback_data="rec_weekdays")],
                [InlineKeyboardButton(text="По выходным", callback_data="rec_weekends")],
                [InlineKeyboardButton(text="Раз в неделю", callback_data="rec_weekly")]
            ])
            await message.answer("🔄 Как часто напоминать?", reply_markup=kb)
            await state.set_state(RemindForm.waiting_for_recurrence)
        else:
            await message.answer("❓ У тебя нет задачи под таким номером.")

@router.callback_query(RemindForm.waiting_for_recurrence)
async def process_recurrence(callback: types.CallbackQuery, state: FSMContext):
    recurrence = callback.data.split("_")[1]
    await state.update_data(recurrence=recurrence)
    
    rec_texts = {
        "none": "Единожды",
        "daily": "Каждый день",
        "weekdays": "По будням",
        "weekends": "По выходным",
        "weekly": "Раз в неделю"
    }
    
    async with get_session() as session:
        result = await session.execute(select(User).filter_by(id=callback.from_user.id))
        user = result.scalars().first()
        tz_offset = user.timezone if user else 0

    await callback.message.edit_text(
        f"Выбрано: *{rec_texts.get(recurrence)}*.\n"
        f"Теперь напиши время в формате ЧЧ:ММ (например, 14:30).\n"
        f"У тебя установлен часовой пояс: *UTC {tz_offset:+}*.",
        parse_mode="Markdown"
    )
    await state.set_state(RemindForm.waiting_for_time)

@router.message(RemindForm.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("❌ Настройка напоминания отменена.")
        return

    try:
        h, m = map(int, message.text.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError()
    except ValueError:
        await message.answer("⚠️ Неверный формат! Введи время в виде ЧЧ:ММ (до 23:59).")
        return

    data = await state.get_data()
    task_id = data.get("task_id")
    recurrence = data.get("recurrence")

    now_utc = datetime.utcnow()

    async with get_session() as session:
        result = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = result.scalars().first()
        tz_offset = user.timezone if user else 0
        
        remind_at = calculate_initial_remind_time(now_utc, h, m, tz_offset, recurrence)

        task_res = await session.execute(select(Task).filter(Task.id == task_id))
        task = task_res.scalars().first()
        if task:
            task.remind_at = remind_at
            task.recurrence = recurrence
            await message.answer(f"✅ Готово! Напомню о задаче '{task.description}' в {h:02d}:{m:02d} (по твоему времени).")
        else:
            await message.answer("❌ Ошибка: задача не найдена.")
            
    await state.clear()
