from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

# 防止睡眠
def DoNotSleep():
    url = "https://line-bot-python-flask-97ly.onrender.com"
    r = requests.get(url)

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='doNotSleeps_job', minutes=20)

sched.start()