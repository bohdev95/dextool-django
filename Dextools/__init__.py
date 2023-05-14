# # from .celery import app as celery_app

# # __all__ = ('celery_app',)

# # from huey.contrib.djhuey import crontab
# # from huey.contrib.djhuey import periodic_task
# # from huey.contrib.djhuey.models import PeriodicTask

# # # The task function that will be run every 5 minutes
# # @huey.task()
# # def my_task():
# #     # Your task logic here
# #     print('hello')

# # # Schedule the task to run every 5 minutes
# # # PeriodicTask.schedule(my_task.s(),every=crontab(minute='*/5'))

# from huey import crontab
# from huey.contrib.djhuey import periodic_task, task

# import requests
# import datetime
# # from .app.models import *

# # @task()
# # def count_beans(number):
# #     print('-- counted %s beans --' % number)
# #     return 'Counted %s beans' % number

# @periodic_task(crontab(minute='*/1'))
# def every_five_mins():
#     print('Every five minutes this will be printed by the consumer')