from flask import Flask, request, jsonify

app = Flask(__name__)

# וודא שהטוקן הזה זהה לחלוטין לטוקן שמופיע לך בממשק המשתמש של eBay
VERIFICATION_TOKEN = "sellpilot_prod_verification_token_92ZxhG3lqpV8yRjKLtA7eXpJmFbNsWdHqC0UvYMtA9BrKw"

@app.route("/notifications", methods=["POST"]) # שינוי ל-POST
def handle_ebay_notification():
    # 1. בדוק שהבקשה היא POST
    if request.method == "POST":
        # 2. נסה לפרסר את גוף הבקשה כ-JSON
        try:
            data = request.get_json()
            if data is None: # אם ה-body לא JSON, נסה אולי form data
                data = request.form
        except Exception as e:
            # אם יש שגיאה בפירסור JSON, כנראה שהבקשה לא בפורמט הנכון
            print(f"Error parsing JSON: {e}")
            return "Bad Request: Invalid JSON", 400

        # 3. חפש את ה-challengeCode בנתונים שהתקבלו
        # לפי התיעוד של eBay, זה אמור להגיע כ-challengeCode
        challenge_code_from_ebay = data.get("challengeCode")

        if challenge_code_from_ebay:
            # 4. אם קיבלנו challengeCode, נחזיר אותו חזרה בפורמט הנדרש
            # eBay מצפה ל-challengeResponse באותה בקשה לאימות
            return jsonify({"challengeResponse": challenge_code_from_ebay}), 200
        else:
            # 5. אם לא קיבלנו challengeCode, זה יכול להיות הודעת אירוע רגילה מ-eBay
            # או בקשת אימות שגויה. במקרה כזה, כדאי לטפל באירועים
            # או להחזיר שגיאה אם זה לא אימות.
            print("Received a POST request without challengeCode. This might be a regular event notification.")
            # כאן תוכל להוסיף לוגיקה לטיפול בהודעות אירוע אחרות מ-eBay
            return "OK", 200 # או 204 No Content

    # אם הבקשה אינה POST (למרות שהגדרנו רק POST ב-decorator, זה קוד הגנה)
    return "Method Not Allowed", 405

if __name__ == "__main__":
    # ב-Render, הפורט מוגדר על ידי משתנה סביבה.
    # חשוב להשתמש בו כדי שהאפליקציה תקשיב לפורט הנכון.
    import os
    port = int(os.environ.get("PORT", 5000)) # 5000 הוא ברירת מחדל אם PORT לא מוגדר
    app.run(host="0.0.0.0", port=port) # חשוב להקשיב ל-0.0.0.0
