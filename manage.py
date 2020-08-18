import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app
from backend.models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # print('port: ', port)
    manager.run()
    # -w 2 -b 0.0.0.0:3000
