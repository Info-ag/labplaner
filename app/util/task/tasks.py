from app import create_app
from app.util.task import huey

# Alternative @huey.periodic_task(crontab(day_of_week='1'))
@huey.task()
def example(example_param):
    """Example session
    """
    app, db = create_app(None, minimal=True)
    with app.app_context():
        # Do something
        pass
