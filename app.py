from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Ruta para la base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones

# Configuración de SQLAlchemy
db = SQLAlchemy(app)

# Modelo Todo para la tabla en la base de datos
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Crear las tablas en la base de datos si no existen aún
with app.app_context():
    db.create_all()

# Ruta principal para renderizar el template index.html
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Hubo un problema al agregar la tarea.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Comprobar si se está ejecutando directamente este archivo
if __name__ == "__main__":
    # Iniciar la aplicación Flask en modo debug
    app.run(debug=True)
