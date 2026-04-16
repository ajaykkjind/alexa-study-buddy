from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 🔑 Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this environment variable before running the app

@app.route("/", methods=["GET"])
def home():
    return "Alexa Study Buddy is running!"


@app.route("/alexa", methods=["POST"])
def alexa():
    req = request.json

    # 🔍 Extract question safely
    try:
        intent = req['request']['intent']
        question = intent['slots']['question']['value']
    except:
        question = "Please repeat the question"

    # 🧠 ChatGPT response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"""
You are a class 8 tutor.
Explain in Hinglish.
Keep answer under 3-4 lines.
Use simple words for class 8 students.
Keep answers short, simple, and correct.
Give one examples.

Question: {question}
"""
            }],
            max_tokens=150
        )

        answer = response['choices'][0]['message']['content']

    except Exception as e:
        answer = "Sorry, mujhe abhi problem aa rahi hai. Dubara pucho."

    # 🗣️ Alexa response format
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


if __name__ == "__main__":
    app.run(debug=True)
