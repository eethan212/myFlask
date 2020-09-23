import os
from flask_migrate import MigrateCommand
from flask_script import Manager

from myflask.run import create_app

env = os.environ.get('FLASK_ENV', 'default')

app = create_app(env)

# flask-script 配合 flask-migrate
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
