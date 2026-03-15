import logging
from pathlib import Path
import json
from typing import Dict, List

logger = logging.getLogger("LucyPlugins")

class PluginManager:
    def __init__(self):
        self.plugins_dir = Path(__file__).parent.parent / "plugins"
        self.config_path = self.plugins_dir.parent / "plugin_config.json"
        self.plugins = {}
        self.enabled_plugins = []
        self._load_config()
        logger.info(f"🔌 Plugin Manager Initialized")

    def _load_config(self):
        """Load plugin configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.enabled_plugins = config.get('enabled', [])
                    logger.info(f"✅ Loaded {len(self.enabled_plugins)} enabled plugins")
            else:
                # Default enabled plugins
                self.enabled_plugins = ['voice', 'vision', 'web', 'filesystem']
                self._save_config()
        except Exception as e:
            logger.error(f"Load config error: {e}")
            self.enabled_plugins = ['voice', 'vision', 'web', 'filesystem']

    def _save_config(self):
        """Save plugin configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump({'enabled': self.enabled_plugins}, f, indent=2)
        except Exception as e:
            logger.error(f"Save config error: {e}")

    def get_available_plugins(self) -> List[dict]:
        """Get list of available plugins"""
        return [
            {"id": "voice", "name": "Voice", "description": "Text-to-speech and speech recognition", "enabled": "voice" in self.enabled_plugins},
            {"id": "vision", "name": "Vision", "description": "Image and screen analysis", "enabled": "vision" in self.enabled_plugins},
            {"id": "web", "name": "Web", "description": "Web browsing and summarization", "enabled": "web" in self.enabled_plugins},
            {"id": "filesystem", "name": "File System", "description": "Read and write files", "enabled": "filesystem" in self.enabled_plugins},
            {"id": "autonomy", "name": "Autonomy", "description": "Self-thinking and goals", "enabled": "autonomy" in self.enabled_plugins},
            {"id": "memory", "name": "Memory", "description": "Long-term conversation memory", "enabled": "memory" in self.enabled_plugins},
        ]

    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin"""
        if plugin_id not in self.enabled_plugins:
            self.enabled_plugins.append(plugin_id)
            self._save_config()
            logger.info(f"✅ Enabled plugin: {plugin_id}")
            return True
        return False

    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin"""
        if plugin_id in self.enabled_plugins:
            self.enabled_plugins.remove(plugin_id)
            self._save_config()
            logger.info(f"⏸️ Disabled plugin: {plugin_id}")
            return True
        return False

    def is_enabled(self, plugin_id: str) -> bool:
        """Check if plugin is enabled"""
        return plugin_id in self.enabled_plugins

plugin_manager = PluginManager()