from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Load sensitive data from environment variables
# הטוקן שהתקבל ממך מוטמע ישירות בקוד:
VERIFICATION_TOKEN = "sellpilot_prod_verification_token_92ZxhG3lqpV8yRjKLtA7eXpJmFbNsWdHqC0UvYMtA9BrKw"

# חשוב: endpoint_url צריך להיות ה-URL המלא של ה-endpoint שלך ב-Render
# שהיה https://sellpilot-api.onrender.com/notifications
ENDPOINT_URL = "https://sellpilot-api.onrender.com/notifications"


@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if request.method == 'GET':
        challenge_code = request.args.get('challenge_code')
        if challenge_code:
            print(f"Received GET verification request with challenge_code: {challenge_code}")
            print(f"Using VERIFICATION_TOKEN: {VERIFICATION_TOKEN}")
            print(f"Using ENDPOINT_URL: {ENDPOINT_URL}")

            # יצירת המחרוזת ל-hashing לפי הסדר: challengeCode + verificationToken + endpoint
            string_to_hash = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
            
            # ביצוע ה-hashing ב-SHA256
            m = hashlib.sha256()
            m.update(string_to_hash.encode('utf-8')) # ודא קידוד ל-UTF-8
            challenge_response_hash = m.hexdigest()

            print(f"Generated challengeResponse hash: {challenge_response_hash}")

            return jsonify({"challengeResponse": challenge_response_hash}), 200, {'Content-Type': 'application/json'}
        else:
            print("Received GET request without challenge_code.")
            return "GET request received, but no challenge_code provided.", 200

    elif request.method == 'POST':
        # זה ה-handler עבור הודעות webhook אמיתיות לאחר האימות
        data = request.get_json()
        if data:
            print(f"Received POST notification: {data}")
            # כאן תוסיף את הלוגיקה לעיבוד ההתראה
            # למשל, שמירת הנתונים למסד נתונים, מחיקת נתוני משתמש וכו'.
            # זכור לטפל גם באימות חתימת ה-Webhook אם אתה רוצה לוודא שזה מגיע מ-eBay.
            # (ראה חלק "Verifying the validity of an eBay marketplace account deletion/closure notification" בתיעוד)
            return "Notification received and processed.", 200
        else:
            print("Received empty POST request or non-JSON POST request.")
            return "Bad Request: No JSON data received or invalid Content-Type for POST.", 400

if __name__ == '__main__':
    # וודא שהפורט הוא 10000 כפי ש-Render מצפה
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
