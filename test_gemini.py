import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6JXU5dpEGMsdvqfkyzEwNEqx4gBGJ7ZwSfrxC4whtv19Q")

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Hello")
print(response.text)
