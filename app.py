from selenium import webdriver
from openai import OpenAI
import base64
from dotenv import load_dotenv
import os

# load environment variable from .env file
load_dotenv()

# Get the secret key from from environment variables
#secret_key = os.gentenv('OPEN_API_KEY)

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://www.linkedin.com/in/bhattacharjee-avishek/")

# Take a screenshot and save it as screenshot.png
driver.save_screenshot('avi1.png')

# Quit the webdriver session
driver.quit()

client = OpenAI(api_key = 'sk-proj-KmLM8dGInw1m38HFFbLrT3BlbkFJeKJ4up5hpgj9CLpEc8K7')

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
base64_image = encode_image('avi1.png')

response = client.chat.completions.create(
    model = 'gpt-4o',
    messages = [
        {
            "role" : "system",
            "content" : [
                {
                "type" : "text",
                "text" : """
                 You're a head hunter for a CTO position. Please extract the most important facts about the candidate.
                 Respond in JSON format.
                 """
                }     
            ]
        },
        {
            "role" : "user",
            "content" : [
                {
                    "type" : "image_url",
                    "image_url" : {
                        "url" : f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        },
        {
            "role" : "assistant",
            "content" : [
                {
                    "type" : "text",
                    "text" : "Here are some observation and recommendations to enhance conversion rates on this webpage: "
                }
            ]
        }
    ],
    temperature = 1,
    max_tokens = 256,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
)

print(response.choices[0].message.content)