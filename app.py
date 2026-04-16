from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 🔑 API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET"])
def home():
    return "Alexa Study Buddy is running!"


@app.route("/alexa", methods=["POST"])
def alexa():
    req = request.json

    try:
        req_type = req['request']['type']
    except:
        req_type = None

    # 🟢 1. Launch request (when user says "open Study Buddy")
    if req_type == "LaunchRequest":
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Namaste! Main Study Buddy hoon. Aap kya padhna chahte ho?"
                },
                "shouldEndSession": False
            }
        })

    # 🔵 2. Intent request (user asks question)
    if req_type == "IntentRequest":
        try:
            intent = req['request']['intent']
            question = intent['slots']['question']['value']
        except:
            question = None

        if not question:
            return jsonify({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Please apna question fir se bolo."
                    },
                    "shouldEndSession": False
                }
            })

        try:
            # 🧠 ChatGPT call
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""
You are a class 8 tutor.

Rules:
- Explain in Hinglish (mix Hindi + English)
- Keep answer short (3-4 lines max)
- Use simple words
- Give 1 example
- Be factually correct (NCERT level)
- If unsure, say: "Mujhe isme doubt hai"

Question: {question}
"""
                }],
                max_tokens=150
            )

            answer = response['choices'][0]['message']['content']

            # ✂️ limit answer length for Alexa
            answer = answer[:300]

        except Exception as e:
            answer = "Sorry, mujhe abhi problem aa rahi hai. Thodi der baad try karo."

        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": answer
                },
                "shouldEndSession": True
            }
        })

    # 🔴 3. Fallback
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Sorry, mujhe samajh nahi aaya."
            },
            "shouldEndSession": True
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
