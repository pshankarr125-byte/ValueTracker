import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# --- GEMINI SETUP ---
# REPLACE THIS WITH YOUR REAL AIza... KEY

API_KEY = os.getenv("AIzaSyB4wfebEu8hSD0SHatFWByP21GUcFgaE1E")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])  
def index():
    ai_advice = None 

    if request.method == 'POST':
        # Grab all the data, including the emotion!
        budget = request.form.get('budget')
        goal_name = request.form.get('goal_name')
        target = request.form.get('target')
        item = request.form.get('item')
        cost = request.form.get('cost')
        emotion = request.form.get('emotion')
        
        # Translate the emoji into a mood for the AI
        mood = "happy" if emotion == "😊" else "neutral" if emotion == "😐" else "guilty/sad"
        
        # The complete, context-rich prompt
        prompt = (f"My monthly budget is ₹{budget}. I am saving for a '{goal_name}' (Target: ₹{target}). "
                  f"I just bought '{item}' for ₹{cost}. I feel {mood} ({emotion}) about this purchase. "
                  f"Act as a financial coach. Analyze this purchase based on my goals, budget, and my emotional state. "
                  f"Give me 2-3 short, punchy sentences of personalized advice.")
        
        try:
            response = model.generate_content(prompt)
            ai_advice = response.text
        except Exception as e:
            ai_advice = f"⚠️ AI Error: Check your API key. (Details: {str(e)})"

    return render_template('index.html', ai_advice=ai_advice)

if __name__ == '__main__':
    app.run(debug=True)
