from apscheduler.schedulers.background import BackgroundScheduler
from dump_user import create_dump

scheduler = BackgroundScheduler()


def run_jobs():
    scheduler.start()


def add_jobs():
    scheduler.add_job(create_dump, 'interval', minutes=1)
