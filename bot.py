import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import BOT_TOKEN, CHANNEL_ID
import content as ct

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Minsk")


async def send(text: str):
    try:
        await bot.send_message(CHANNEL_ID, text)
        log.info("Sent OK")
    except Exception as e:
        log.error("Send error: %s", e)


async def job_morning():
    await send(await ct.morning_digest())


async def job_music():
    await send(await ct.get_music_prompt())


async def job_recipe():
    await send(await ct.get_recipe())


async def job_fact():
    await send(await ct.get_history_fact())


async def job_night():
    await send(await ct.get_goodnight())


def schedule_jobs():
    scheduler.add_job(job_morning, CronTrigger(hour=9, minute=0))
    scheduler.add_job(job_music, CronTrigger(hour=12, minute=0))
    scheduler.add_job(job_recipe, CronTrigger(hour=15, minute=0))
    scheduler.add_job(job_fact, CronTrigger(hour=18, minute=0))
    scheduler.add_job(job_night, CronTrigger(hour=21, minute=0))


async def main():
    schedule_jobs()
    scheduler.start()
    log.info("Bot started. Waiting for jobs...")
    try:
        await asyncio.Event().wait()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
