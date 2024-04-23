import requests

def query_chatgpt(prompt, api_key="sk-proj-8odsSu7lpWuGkB2UDQNeT3BlbkFJiXkOZdFBTIWlWmPCeltP"):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",  # Using an accessible model
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response=response.json()
    # print(response)
    return response['choices'][0]['message']['content']

# Example usage
# prompt = "Hello, who are you?"
# response = query_chatgpt(prompt)
# print(response)
