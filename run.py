from app import app
from flask_cors import CORS

CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)