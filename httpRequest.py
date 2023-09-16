import subprocess
import json

def read_text_file(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def generate_prompt(text):
    # Modify this function to generate a prompt based on the text read from the file
    return f"Render a minimalistic bedroom based on the following description: {text}"

def send_curl_request(prompt):
    data = json.dumps({"prompt": prompt})
    cmd = [
        'curl',
        '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '--data', data,
        'http://430e-35-204-47-149.ngrok.io/generate_image',
        '-o', 'space.jpg'
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    text = read_text_file('test.txt')
    prompt = generate_prompt(text)
    send_curl_request(prompt)