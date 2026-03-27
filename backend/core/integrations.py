"""
Integration Module - Ties all components together and registers them with the kernel.

This module provides:
- Component registration with the kernel
- Cross-module communication interfaces
- Lifecycle management for integrated components
- Unified external system interfaces
"""

import logging
import inspect
from typing import Callable, Any, Dict, List, Optional, Type, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import weakref

from .kernel import app

# Type alias for FastAPI app
KernelType = Any

# Configure logging
logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Types of integrations available."""
    VOICE = auto()
    KNOWLEDGE = auto()
    PROACTIVE = auto()
    NEURAL_VISUALIZATION = auto()
    TEMPORAL_MEMORY = auto()
    AI_EVOLUTION = auto()
    COGNITIVE_LOAD = auto()
    DREAM_MODE = auto()
    REALITY_SIMULATION = auto()
    EMOTIONAL_CONTAGION = auto()
    PHILOSOPHICAL_REASONING = auto()
    CREATIVE_SYNTHESIS = auto()
    IDENTITY_VERIFICATION = auto()
    EXTERNAL_API = auto()
    PLUGIN = auto()


@dataclass
class IntegrationConfig:
    """Configuration for an integration."""
    name: str
    integration_type: IntegrationType
    priority: int = 0
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.name)


class IntegrationRegistry:
    """Registry for managing all integrations."""
    
    def __init__(self, kernel: Any):
        self.kernel = kernel
        self._integrations: Dict[str, IntegrationConfig] = {}
        self._integration_instances: Dict[str, weakref.ref] = {}
        self._registration_callbacks: List[Callable] = []
        self._unregistration_callbacks: List[Callable] = []
    
    def register(self, config: IntegrationConfig, instance: Any = None) -> bool:
        """
        Register a new integration with the kernel.
        
        Args:
            config: Integration configuration
            instance: Optional instance of the integration
            
        Returns:
            True if registration was successful
        """
        if config.name in self._integrations:
            logger.warning(f"Integration '{config.name}' already registered, overwriting...")
        
        self._integrations[config.name] = config
        
        if instance is not None:
            self._integration_instances[config.name] = weakref.ref(instance)
        
        # Notify kernel of new integration
        self.kernel.on('integration_registered',
            {'name': config.name, 'type': config.integration_type}
        )
        
        # Execute registration callbacks
        for callback in self._registration_callbacks:
            try:
                callback(config.name, config)
            except Exception as e:
                logger.error(f"Error in registration callback: {e}")
        
        logger.info(f"Registered integration: {config.name} ({config.integration_type})")
        return True
    
    def unregister(self, name: str) -> bool:
        """
        Unregister an integration.
        
        Args:
            name: Name of the integration to unregister
            
        Returns:
            True if integration was found and unregistered
        """
        if name not in self._integrations:
            return False
        
        config = self._integrations.pop(name)
        
        # Notify kernel
        self.kernel.event_bus.publish(
            'integration_unregistered',
            {'name': name, 'type': config.integration_type}
        )
        
        # Execute unregistration callbacks
        for callback in self._unregistration_callbacks:
            try:
                callback(name, config)
            except Exception as e:
                logger.error(f"Error in unregistration callback: {e}")
        
        # Clean up instance reference
        if name in self._integration_instances:
            del self._integration_instances[name]
        
        logger.info(f"Unregistered integration: {name}")
        return True
    
    def get(self, name: str) -> Optional[IntegrationConfig]:
        """Get integration configuration by name."""
        return self._integrations.get(name)
    
    def get_all(self) -> List[IntegrationConfig]:
        """Get all registered integrations."""
        return list(self._integrations.values())
    
    def is_registered(self, name: str) -> bool:
        """Check if an integration is registered."""
        return name in self._integrations
    
    def add_registration_callback(self, callback: Callable[..., Any]) -> None:
        """Add a callback to be called when an integration is registered."""
        self._registration_callbacks.append(callback)
    
    def add_unregistration_callback(self, callback: Callable[..., Any]) -> None:
        """Add a callback to be called when an integration is unregistered."""
        self._unregistration_callbacks.append(callback)
    
    def clear_all(self) -> None:
        """Clear all registered integrations."""
        for name in list(self._integrations.keys()):
            self.unregister(name)


class IntegrationManager:
    """Manages the lifecycle and execution of integrations."""
    
    def __init__(self, registry: IntegrationRegistry):
        self.registry = registry
        self._execution_order: List[str] = []
        self._active_integrations: Set[str] = set()
    
    def initialize(self) -> None:
        """Initialize all registered integrations in priority order."""
        integrations = sorted(
            self.registry.get_all(),
            key=lambda x: x.priority,
            reverse=True
        )
        
        for config in integrations:
            if config.enabled:
                self._activate(config.name)
    
    def _activate(self, name: str) -> None:
        """Activate a specific integration."""
        if name in self._active_integrations:
            return
        
        config = self.registry.get(name)
        if not config:
            return
        
        try:
            # Initialize integration-specific setup
            self._initialize_integration(name, config)
            self._active_integrations.add(name)
            logger.info(f"Activated integration: {name}")
        except Exception as e:
            logger.error(f"Error activating integration {name}: {e}")
            self._deactivate(name)
    
    def _deactivate(self, name: str) -> None:
        """Deactivate a integration."""
        if name in self._active_integrations:
            self._active_integrations.discard(name)
            logger.info(f"Deactivated integration: {name}")
    
    def _initialize_integration(self, name: str, config: IntegrationConfig) -> None:
        """
        Initialize a specific integration.
        
        This is where integration-specific setup happens.
        """
        # Default initialization - subclasses can override
        pass
    
    def execute(self, name: str, *args, **kwargs) -> Any:
        """
        Execute an integration's main function.
        
        Args:
            name: Name of the integration
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Result of the integration execution
        """
        config = self.registry.get(name)
        if not config or not config.enabled:
            logger.warning(f"Integration '{name}' not found or disabled")
            return None
        
        # Execute in priority order
        if name not in self._execution_order:
            self._execution_order.append(name)
        
        try:
            result = self._execute_integration(name, *args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing integration {name}: {e}")
            return None
    
    def _execute_integration(self, name: str, *args, **kwargs) -> Any:
        """
        Execute a specific integration.
        
        Override this method in subclasses to provide custom execution logic.
        """
        # Default implementation - return None
        return None
    
    def get_active_count(self) -> int:
        """Get the number of currently active integrations."""
        return len(self._active_integrations)
    
    def get_active_names(self) -> List[str]:
        """Get names of all active integrations."""
        return list(self._active_integrations)


class IntegrationPoint:
    """
    A point where multiple integrations can interact.
    
    This provides a way for different components to communicate
    through a shared interface.
    """
    
    def __init__(self, name: str, kernel: KernelType):
        self.name = name
        self.kernel = kernel
        self._handlers: List[Callable[..., Any]] = []
        self._config: Dict[str, Any] = {}
    
    def register_handler(self, handler: Callable[..., Any]) -> None:
        """Register a handler for this integration point."""
        self._handlers.append(handler)
        logger.debug(f"Registered handler for integration point: {self.name}")
    
    def unregister_handler(self, handler: Callable[..., Any]) -> None:
        """Unregister a handler from this integration point."""
        if handler in self._handlers:
            self._handlers.remove(handler)
            logger.debug(f"Unregistered handler from integration point: {self.name}")
    
    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        """Invoke all registered handlers."""
        results = []
        for handler in self._handlers:
            try:
                result = handler(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Handler error in integration point {self.name}: {e}")
        return results if results else None
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set configuration for this integration point."""
        self._config.update(config)
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self._config.copy()


class IntegrationBus:
    """
    Message bus for inter-integration communication.
    
    Provides a pub/sub pattern for integrations to communicate
    with each other.
    """
    
    def __init__(self, kernel: KernelType):
        self.kernel = kernel
        self._subscribers: Dict[str, List[Callable[..., Any]]] = {}
        self._topics: Set[str] = set()
    
    def subscribe(self, topic: str, callback: Callable[..., Any]) -> None:
        """Subscribe to a topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)
        self._topics.add(topic)
        logger.debug(f"Subscribed to topic: {topic}")
    
    def unsubscribe(self, topic: str, callback: Callable[..., Any]) -> None:
        """Unsubscribe from a topic."""
        if topic in self._subscribers:
            if callback in self._subscribers[topic]:
                self._subscribers[topic].remove(callback)
                logger.debug(f"Unsubscribed from topic: {topic}")
    
    def publish(self, topic: str, data: Any) -> None:
        """Publish data to all subscribers of a topic."""
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in subscriber callback: {e}")
        else:
            logger.debug(f"Published to new topic: {topic}")
            self._topics.add(topic)
    
    def get_topics(self) -> List[str]:
        """Get list of all topics."""
        return list(self._topics)
    
    def clear(self) -> None:
        """Clear all subscriptions and topics."""
        self._subscribers.clear()
        self._topics.clear()


# Global instances
_kernel: Optional[Kernel] = None
_registry: Optional[IntegrationRegistry] = None
_manager: Optional[IntegrationManager] = None
_bus: Optional[IntegrationBus] = None


def set_kernel(kernel: "Kernel") -> None:
    """Set the global kernel instance."""
    global _kernel
    _kernel = kernel


def get_kernel() -> Optional["Kernel"]:
    """Get the global kernel instance."""
    return _kernel


def set_registry(registry: IntegrationRegistry) -> None:
    """Set the global registry instance."""
    global _registry
    _registry = registry


def get_registry() -> Optional[IntegrationRegistry]:
    """Get the global registry instance."""
    return _registry


def set_manager(manager: IntegrationManager) -> None:
    """Set the global manager instance."""
    global _manager
    _manager = manager


def get_manager() -> Optional[IntegrationManager]:
    """Get the global manager instance."""
    return _manager


def set_bus(bus: IntegrationBus) -> None:
    """Set the global bus instance."""
    global _bus
    _bus = bus


def get_bus() -> Optional[IntegrationBus]:
    """Get the global bus instance."""
    return _bus


def initialize_integrations(kernel: Kernel) -> None:
    """
    Initialize the integration system with the given kernel.
    
    This should be called early in the application lifecycle.
    """
    global _kernel, _registry, _manager, _bus
    
    _kernel = kernel
    _registry = IntegrationRegistry(kernel)
    _manager = IntegrationManager(_registry)
    _bus = IntegrationBus(kernel)
    
    # Register default integration points
    _register_default_points()
    
    # Initialize all integrations
    _manager.initialize()
    
    logger.info("Integration system initialized")


def _register_default_points() -> None:
    """Register default integration points."""
    default_points = [
        'voice_input',
        'knowledge_query',
        'proactive_action',
        'neural_display',
        'temporal_sync',
        'evolution_trigger',
        'load_monitor',
        'dream_cycle',
        'reality_check',
        'emotion_response',
        'philosophy_engine',
        'creative_output',
        'identity_check',
    ]
    
    for point_name in default_points:
        IntegrationPoint(point_name, _kernel or app)


def create_integration_config(
    name: str,
    integration_type: IntegrationType,
    priority: int = 0,
    config: Optional[Dict[str, Any]] = None
) -> IntegrationConfig:
    """
    Create a new integration configuration.
    
    Args:
        name: Unique name for the integration
        integration_type: Type of integration
        priority: Execution priority (higher = earlier)
        config: Additional configuration data
        
    Returns:
        New IntegrationConfig instance
    """
    if config is None:
        config = {}
    
    return IntegrationConfig(
        name=name,
        integration_type=integration_type,
        priority=priority,
        config=config
    )


def register_integration(
    config: IntegrationConfig,
    instance: Any = None
) -> bool:
    """
    Convenience function to register an integration.
    
    Args:
        config: Integration configuration
        instance: Optional instance of the integration
        
    Returns:
        True if registration was successful
    """
    if _registry is None:
        logger.error("Integration registry not initialized. Call initialize_integrations() first.")
        return False
    
    return _registry.register(config, instance)


def unregister_integration(name: str) -> bool:
    """
    Convenience function to unregister an integration.
    
    Args:
        name: Name of the integration to unregister
        
    Returns:
        True if integration was found and unregistered
    """
    if _registry is None:
        logger.error("Integration registry not initialized.")
        return False
    
    return _registry.unregister(name)


def execute_integration(name: str, *args, **kwargs) -> Any:
    """
    Convenience function to execute an integration.
    
    Args:
        name: Name of the integration
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
            Result of the integration execution
    """
    if _manager is None:
        logger.error("Integration manager not initialized.")
        return None
    
    return _manager.execute(name, *args, **kwargs)


def subscribe_to_topic(topic: str, callback: Callable) -> None:
    """
    Convenience function to subscribe to a topic.
    
    Args:
        topic: Topic to subscribe to
        callback: Callback function to invoke when topic is published
    """
    if _bus is None:
        logger.error("Integration bus not initialized.")
        return
    
    _bus.subscribe(topic, callback)


def publish_to_topic(topic: str, data: Any) -> None:
    """
    Convenience function to publish to a topic.
    
    Args:
        topic: Topic to publish to
        data: Data to publish
    """
    if _bus is None:
        logger.error("Integration bus not initialized.")
        return
    
    _bus.publish(topic, data)