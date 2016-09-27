#!.venv/bin/python
from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import User, Kedves

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
app.debug=True

def make_shell_context():
  return dict(app=app, db=db, User=User, Kedves=Kedves)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
  manager.run()
