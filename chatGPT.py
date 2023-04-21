import openai
openai.api_key = "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"

# response = openai.Image.create(
#   prompt="AI",
#   n=1,
#   size="1024x1024"
# )
# image_url = response['data'][0]['url']
# print(image_url)

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

msg = response['choices'][0]['message']['content']

print(msg)
