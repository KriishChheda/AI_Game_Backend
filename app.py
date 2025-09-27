from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Initial game state
game_state = {
    "blocks": [
        {"x": 100, "y": 200, "score": 1},
        {"x": 150, "y": 180, "score": 1},
        {"x": 200, "y": 160, "score": 1},
    ],
    "birds_left": 5,
}

@app.route("/apply_shot", methods=["POST", "OPTIONS"])
def apply_shot():
    # Preflight requests (OPTIONS) are automatically handled by Flask-CORS
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json() or {}
    angle = data.get("angle", 0)
    velocity = data.get("velocity", 0)
    state = data.get("state", game_state)

    # Dummy logic: move blocks down by velocity
    for block in state.get("blocks", []):
        block["y"] += velocity

    # Decrement birds left
    state["birds_left"] = max(state.get("birds_left", 0) - 1, 0)

    return jsonify({"new_state": state})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
