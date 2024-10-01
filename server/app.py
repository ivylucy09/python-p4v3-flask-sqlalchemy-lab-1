#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)  # Update this line
    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)

# Add views here
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query earthquakes with magnitude >= provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Format the response data
    quakes_data = [
        {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        for earthquake in earthquakes
    ]

    # Construct the JSON response with the count and the list of earthquakes
    response = {
        "count": len(quakes_data),
        "quakes": quakes_data
    }

    # Return the response with a 200 OK status
    return jsonify(response), 200