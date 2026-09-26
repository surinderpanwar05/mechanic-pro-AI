import os
import importlib

def get_provider():
    provider_name = os.getenv("AI_PROVIDER", "gemini").lower()

    module = importlib.import_module(
        f"app.providers.{provider_name}"
    )

    class_name = "".join(
        word.capitalize()
        for word in provider_name.split("_")
    ) + "Provider"

    provider_class = getattr(module, class_name)

    return provider_class()
