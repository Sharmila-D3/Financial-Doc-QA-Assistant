import requests

class OllamaClient:
    def __init__(self, model_name="llama2:latest"):
        self.base_url = "http://localhost:11434"
        self.model_name = model_name

    def query(self, prompt):
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "[No response]")
        except Exception as e:
            return f"Error communicating with Ollama: {e}"
