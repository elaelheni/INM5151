from economeuble import app, db
from economeuble.database import User, Article

#Script pour créer une base de données
@app.shell_context_processor
def make_shell_context():
	return dict(app=app, db=db, User=User, Article=Article)
