from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "sellpilot_prod_verification_token_92ZxhG3lqpV8yRjKLtA7eXpJmFbNsWdHqC0UvYMtA9BrKw" # שים כאן את הטוקן מאיביי

@app.route("/notifications", methods=["GET"])
def verify():
    challenge_code = request.args.get("challenge_code")
    return jsonify({"challengeResponse": VERIFICATION_TOKEN}), 200

if __name__ == "__main__":
    app.run()
