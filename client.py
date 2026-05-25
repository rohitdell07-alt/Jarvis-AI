from google import genai

# Create client
client = genai.Client(
    api_key="AIzaSyD5VAHrYh-ocZ2UAGICYgGUwbxbbogbnlQ"
)

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""
You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant.

User: What is coding?
"""
)

print(response.text)