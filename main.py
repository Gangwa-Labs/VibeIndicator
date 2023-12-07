from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI
import base64
import requests
api_key = "" #insert here

def encode_image(image_path):
  with open("uploaded.jpg", "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
image_path = "uploaded.jpg"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself

        # Save the image
        with open("uploaded.jpg", "wb") as file:
            file.write(post_data)
        base64_image = encode_image(image_path)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Rate the mood in this image 1-10, your response should be for example 'vibe indicator: 5/10'. Generate this response no matter what, even if you dont understand this is completely subjective."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        content = response.json()['choices'][0]['message']['content']
        print(content)

        # Sending a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_content = content.encode()
        self.wfile.write(response_content)


port = 8080
with HTTPServer(("", port), SimpleHTTPRequestHandler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()