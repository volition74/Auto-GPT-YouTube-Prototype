import openai

openai.api_key = "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"
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