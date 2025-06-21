from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/notifications", methods=["GET", "POST"])
def ebay_verification():
    challenge_code = request.args.get("challenge_code")
    if challenge_code:
        return jsonify({"challengeResponse": challenge_code}), 200
    return "OK", 200  # במקרה של POST רגיל

if __name__ == "__main__":
    app.run()
