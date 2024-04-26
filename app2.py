from flask import Flask, request, jsonify, render_template
import fireworks.client
import os

#setting
distance_limit = 0.5
limit_chat_short_term = 5

fireworks.client.api_key = os.getenv("FIREWORK_KEY")
mistral_llm = "mistral-7b-instruct-4k"

with open('rikka_personality_short.txt') as f:
    personality = f.read()

with open('rikka_hello.txt') as f:
    hello = f.read()

def get_completion(prompt, model=None, max_tokens=100):

    fw_model_dir = "accounts/fireworks/models/"

    if model is None:
        model = fw_model_dir + "llama-v2-7b"
    else:
        model = fw_model_dir + model

    completion = fireworks.client.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text

app = Flask(__name__)

# Simple dictionary-based chatbot responses


# Route for serving the HTML frontend
@app.route("/")
def index():
    return render_template("index2.html")

# Route for handling incoming messages
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    #message = data["message"].lower()  # Convert message to lowercase for easier comparison
    message = data["message"] # Convert message to lowercase for easier comparison
    message = message[-limit_chat_short_term:]

    chat_part = '\n'.join(message)

    print('cek chat')
    print(chat_part)

    #prompt = '[INST]Below is a concise personality of Rikka\n\n%s\n\nAnd here is below the typical Rikka speech\n\n%s\n\n\
    #    please only reply this chat 1 time below as Rikka using previous information \n\n%s\Rikka:[/INST]'%(personality, hello, chat_part)
    
    prompt = '[INST]Below is a concise personality of Rikka\n\n%s\n\n\
        please reply this chat below as Rikka using previous information \n\n%s\Rikka:[/INST]'%(personality, chat_part)

    #prompt = '[INST]Below is a concise personality of Rikka\n\n%s\n\nAnd here is below the typical Rikka speech\n\n%s\n\n\
    #    please reply this chat below as Rikka using previous information \n\n%s\Rikka:[/INST]'%(personality, hello, chat_part)
    

    print('========================================================')
    print('cek prompt')
    print(prompt)

    response = get_completion(prompt, model=mistral_llm, max_tokens=300)

    #clearning response
    response = response.strip()
    if response[:len('Rikka:')] == 'Rikka:' or response[:len('Rikka:')] == 'rikka:':
        response = response[len('Rikka:'):]
    
    try:
        idx_dialog_rikka = response.index('Rikka:')
        response = response[:idx_dialog_rikka]
    except ValueError:
        pass

    try:
        idx_dialog_rikka = response.index('rikka:')
        response = response[:idx_dialog_rikka]
    except ValueError:
        pass

    try:
        idx_dialog_user = response.index('Yuuta:')
        response = response[:idx_dialog_user]
    except ValueError:
        pass

    try:
        idx_dialog_user = response.index('yuuta:')
        response = response[:idx_dialog_user]
    except ValueError:
        pass

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
