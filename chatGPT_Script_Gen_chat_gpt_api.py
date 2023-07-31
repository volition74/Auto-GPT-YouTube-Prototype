import openai

# copy and rename this file to chat_gpt_api.py add in your key to the copy. 
# gitHub repo users --- Add chat_gpt_api.py to your ignore list in your github repo so you don't upload your key
openai.api_key = "sk-yourkey"
selected_model = "gpt-3.5-turbo"

def basic_generation(user_prompt):
    completion = openai.ChatCompletion.create(
        model=selected_model,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response