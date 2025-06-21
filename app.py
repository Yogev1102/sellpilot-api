from flask import Flask, request, jsonify

app = Flask(__name__)

# וודא שהטוקן הזה זהה לחלוטין לטוקן שמופיע לך בממשק המשתמש של eBay
# שימו לב: אורך הטוקן ש-eBay שולחת ב-GET הוא שונה מהטוקן שמוצג בצילום מסך המקורי.
# יש לוודא שהטוקן ב-VERIFICATION_TOKEN הוא בדיוק הטוקן ש-eBay מצפה לו באימות (כלומר, הטוקן הארוך שמסתיים ב-KW)
# אם eBay שולחת טוקן קצר ב-GET, זה אומר שהטוקן שאתה מגדיר בקוד צריך להיות דווקא הקצר.
# אבל על פי הצילום מסך, זה היה הטוקן הארוך: sellpilot_prod_verification_token_92ZxhG3lqpV8yRjKLtA7eXpJmFbNsWdHqC0UvYMtA9BrKw
# בוא נניח שהטוקן הארוך הוא הנכון לאימות הסופי, ושהטוקן הקצר הוא רק לצורך הבדיקה הראשונית שהם עושים ב-GET.
# אם זה לא עובד, נצטרך לבדוק מה eBay באמת מצפה שיוחזר.
VERIFICATION_TOKEN = "sellpilot_prod_verification_token_92ZxhG3lqpV8yRjKLtA7eXpJmFbNsWdHqC0UvYMtA9BrKw"

@app.route("/notifications", methods=["GET", "POST"]) # עכשיו מטפל גם ב-GET וגם ב-POST
def handle_ebay_notification():
    if request.method == "GET":
        # זה נראה שבקשות האימות של eBay מגיעות כ-GET עם challenge_code בפרמטרים
        challenge_code = request.args.get("challenge_code")
        
        if challenge_code:
            print(f"Received GET verification request with challenge_code: {challenge_code}")
            # eBay מצפה שתחזיר את אותו challenge_code שקיבלת,
            # אבל במפתח challengeResponse (לפי התיעוד הכללי של Webhooks)
            # יש גם אפשרות שהם מצפים לטוקן שהוגדר ב-UI. ננסה את מה שקיבלנו.
            return jsonify({"challengeResponse": challenge_code}), 200
        else:
            # אם אין challenge_code ב-GET, זו אולי גישה ישירה לדפדפן או משהו לא צפוי
            print("Received GET request without challenge_code.")
            return "GET request received, but no challenge_code provided.", 200 # או 400

    elif request.method == "POST":
        # זה יהיה עבור הודעות אירועים רגילות ש-eBay תשלח בעתיד
        try:
            data = request.get_json()
            if data is None:
                # אם זה לא JSON, נסה לראות אם זה x-www-form-urlencoded
                data = request.form
            print(f"Received POST request with data: {data}")

            # בדוק אם יש גם challengeCode ב-POST (למקרה ש-eBay שולחת ככה אימות)
            challenge_code_from_post = data.get("challengeCode")
            if challenge_code_from_post:
                print(f"Received POST verification request with challengeCode: {challenge_code_from_post}")
                return jsonify({"challengeResponse": challenge_code_from_post}), 200
            else:
                # לוגיקה לטיפול בהודעות אירועים רגילות מ-eBay
                # לדוגמה: print(data['metadata']['topic'])
                return "POST notification received and processed.", 200 # או 204 No Content

        except Exception as e:
            print(f"Error processing POST request: {e}")
            return "Error processing POST request", 400

# זה לא אמור לקרות אם הגדרת methods=["GET", "POST"]
    return "Method Not Allowed", 405

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
