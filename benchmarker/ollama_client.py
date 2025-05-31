"""
Ollama client for interacting with LLMs through the Ollama API.
"""

import requests
import json
from typing import Optional, Dict, Any
import time


class OllamaClient:
    """Client for communicating with Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def is_available(self) -> bool:
        """Check if Ollama is available and responding."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list:
        """List available models."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.RequestException as e:
            raise Exception(f"Failed to list models: {e}")

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.1,
        timeout: int = 120,
    ) -> str:
        """
        Generate a response from the model.

        Args:
            model: Name of the model to use
            prompt: The prompt to send to the model
            system: Optional system message
            temperature: Sampling temperature (lower = more deterministic)
            timeout: Request timeout in seconds

        Returns:
            The generated response text
        """
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 4096,  # Max tokens to generate
            },
        }

        if system:
            data["system"] = system

        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/generate", json=data, timeout=timeout
            )
            response.raise_for_status()

            result = response.json()
            generation_time = time.time() - start_time

            if "response" not in result:
                raise Exception("No response received from model")

            return result["response"].strip()

        except requests.Timeout:
            raise Exception(f"Request timed out after {timeout} seconds")
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from Ollama")

    def chat(
        self, model: str, messages: list, temperature: float = 0.1, timeout: int = 120
    ) -> str:
        """
        Chat with the model using conversation format.

        Args:
            model: Name of the model to use
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            timeout: Request timeout in seconds

        Returns:
            The generated response text
        """
        data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 4096,
            },
        }

        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/chat", json=data, timeout=timeout
            )
            response.raise_for_status()

            result = response.json()
            generation_time = time.time() - start_time

            if "message" not in result or "content" not in result["message"]:
                raise Exception("No response received from model")

            return result["message"]["content"].strip()

        except requests.Timeout:
            raise Exception(f"Request timed out after {timeout} seconds")
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from Ollama")

    def pull_model(self, model: str) -> bool:
        """
        Pull a model if it's not already available.

        Args:
            model: Name of the model to pull

        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if model already exists
            available_models = self.list_models()
            if model in available_models:
                return True

            # Pull the model
            data = {"name": model}
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json=data,
                timeout=300,  # 5 minutes for model pulling
            )
            response.raise_for_status()
            return True

        except requests.RequestException:
            return False
