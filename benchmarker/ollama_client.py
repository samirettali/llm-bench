"""
Ollama client wrapper using the official ollama Python library.
"""

import ollama
from typing import Optional, List, Dict, Any
import time


class OllamaClient:
    """Client wrapper for the official ollama Python library."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        # Initialize the official ollama client
        self.client = ollama.Client(host=base_url)

    def is_available(self) -> bool:
        """Check if Ollama is available and responding."""
        try:
            # Try to list models to check if service is available
            self.client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List available models."""
        try:
            response = self.client.list()
            return [model["name"] for model in response.get("models", [])]
        except Exception as e:
            raise Exception(f"Failed to list models: {e}")

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.0,
        timeout: int = 120,
    ) -> str:
        """
        Generate a response from the model (legacy method for backward compatibility).

        Args:
            model: Name of the model to use
            prompt: The prompt to send to the model
            system: Optional system message
            temperature: Sampling temperature (lower = more deterministic)
            timeout: Request timeout in seconds

        Returns:
            The generated response text
        """
        try:
            start_time = time.time()

            # Prepare the request options
            options = {
                "temperature": temperature,
                "num_predict": 4096,  # Max tokens to generate
            }

            # Use the official client's generate method
            response = self.client.generate(
                model=model, prompt=prompt, system=system, options=options, stream=False
            )

            generation_time = time.time() - start_time

            if "response" not in response:
                raise Exception("No response received from model")

            return response["response"].strip()

        except ollama.RequestError as e:
            raise Exception(f"Request failed: {e}")
        except ollama.ResponseError as e:
            raise Exception(f"Response error: {e}")
        except Exception as e:
            raise Exception(f"Generation failed: {e}")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        timeout: int = 120,
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
        try:
            start_time = time.time()

            options = {
                "temperature": temperature,
                "num_predict": 4096,
            }

            response = self.client.chat(
                model=model, messages=messages, options=options, stream=False
            )

            generation_time = time.time() - start_time

            if "message" not in response or "content" not in response["message"]:
                raise Exception("No response received from model")

            return response["message"]["content"].strip()

        except ollama.RequestError as e:
            raise Exception(f"Request failed: {e}")
        except ollama.ResponseError as e:
            raise Exception(f"Response error: {e}")
        except Exception as e:
            raise Exception(f"Chat failed: {e}")

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

            # Pull the model using the official client
            self.client.pull(model)
            return True

        except Exception as e:
            print(f"Failed to pull model {model}: {e}")
            return False
