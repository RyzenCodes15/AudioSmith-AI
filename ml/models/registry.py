"""
AudioSmith AI — Model Registry.

Factory pattern for creating speech enhancement model instances.
Maps model names to their concrete implementations.
"""

from __future__ import annotations

from typing import Dict, Type

from ml.models.base import BaseSpeechEnhancer


class ModelRegistry:
    """Registry of available speech enhancement models.

    Uses the factory pattern to decouple model creation from usage.
    The worker task calls `registry.get("deepfilternet")` and never
    imports a specific model class.

    Usage:
        registry = ModelRegistry()
        registry.register("deepfilternet", DeepFilterNetAdapter)
        registry.register("conv_tasnet", ConvTasNetAdapter)

        model = registry.create("deepfilternet")
        model.load()
        enhanced = model.enhance(audio)
    """

    def __init__(self) -> None:
        self._models: Dict[str, Type[BaseSpeechEnhancer]] = {}

    def register(self, name: str, model_class: Type[BaseSpeechEnhancer]) -> None:
        """Register a model class under a given name.

        Args:
            name: Unique identifier for the model.
            model_class: Class that implements BaseSpeechEnhancer.

        Raises:
            ValueError: If a model is already registered under this name.
        """
        if name in self._models:
            raise ValueError(
                f"Model '{name}' is already registered. "
                f"Use a different name or unregister first."
            )
        self._models[name] = model_class

    def unregister(self, name: str) -> None:
        """Remove a model from the registry.

        Args:
            name: Name of the model to remove.

        Raises:
            KeyError: If the model is not registered.
        """
        if name not in self._models:
            raise KeyError(f"Model '{name}' is not registered.")
        del self._models[name]

    def create(self, name: str, **kwargs) -> BaseSpeechEnhancer:
        """Create an instance of a registered model.

        Args:
            name: Name of the registered model.
            **kwargs: Arguments to pass to the model constructor.

        Returns:
            An instance of the requested model.

        Raises:
            KeyError: If the model is not registered.
        """
        if name not in self._models:
            available = ", ".join(sorted(self._models.keys()))
            raise KeyError(
                f"Model '{name}' is not registered. "
                f"Available models: [{available}]"
            )
        return self._models[name](**kwargs)

    def list_models(self) -> list[str]:
        """List all registered model names."""
        return sorted(self._models.keys())

    @property
    def count(self) -> int:
        """Number of registered models."""
        return len(self._models)


# ── Global registry singleton ────────────────────────────────────────────

_registry = ModelRegistry()


def get_registry() -> ModelRegistry:
    """Get the global model registry singleton."""
    return _registry
