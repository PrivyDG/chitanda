from huey.contrib.minimal import MiniHuey

huey = MiniHuey()


@huey.task()
def task():
    pass
