# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
# show route -- display one thing in detail
@app.route('/earthquakes/<int:id>')
def earthquakes(id):
    try: 
        earthquake = Earthquake.query.get(id)
        if not earthquake:
            return {"message": f"Earthquake {id} not found."}, 404 # 404not found
        else:
            return earthquake.to_dict(), 200
    except Exception as e:
        return {"message": str(e)}, 400 #400 is crashed bc something went wrong 


@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    try:
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        earthquakes_match = [earthquake.to_dict() for earthquake in earthquakes]
        response = {
            "count": len(earthquakes_match),
            "quakes": earthquakes_match
        }
        return make_response(response, 200)
    except Exception as e:
        return {"message": str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
