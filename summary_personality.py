from flask import Flask, request, jsonify, render_template
import chromadb
import fireworks.client
import os

fireworks.client.api_key = os.getenv("FIREWORK_KEY")
mistral_llm = "mistral-7b-instruct-4k"

def get_completion(prompt, model=None, max_tokens=1000):

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

with open('rikka_personality.txt') as f:
    raw_personality = f.read()

#print(raw_personality)

prompt = '[INST]please give a concise summarize about this furina personality below\n\n%s\n[/INST]'%(raw_personality)
#print(prompt)

response = get_completion(prompt, model=mistral_llm)
print(response)