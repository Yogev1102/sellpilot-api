from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/notifications", methods=["GET"])
def verify():
    challenge_code = request.args.get("challenge_code")
    return jsonify({"challengeResponse": challenge_code}), 200

if __name__ == "__main__":
    app.run()
