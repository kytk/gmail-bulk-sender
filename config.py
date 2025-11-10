#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Manager for Email Bulk Sender
Handles loading and saving configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration file operations for Email Bulk Sender"""

    CONFIG_VERSION = "2.0"

    def __init__(self, config_type: str = "email"):
        """
        Initialize ConfigManager

        Args:
            config_type: "email" for generic SMTP or "gmail" for Gmail-specific
        """
        self.config_type = config_type

        # Set config directory and file path
        if config_type == "gmail":
            self.config_dir = Path.home() / ".gmail_bulk_sender"
            self.config_file = self.config_dir / "config.json"
        else:
            self.config_dir = Path.home() / ".email_bulk_sender"
            self.config_file = self.config_dir / "config.json"

    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration structure

        Returns:
            Dictionary with default configuration values
        """
        base_config = {
            "version": self.CONFIG_VERSION,
            "sender": {
                "email_address": "",
                "display_name": ""
            },
            "files": {
                "csv_file": "",
                "template_file": "",
                "attachments": []
            },
            "email_options": {
                "cc": "",
                "bcc": "",
                "reply_to": "",
                "send_delay": 5
            },
            "ui": {
                "language": "ja"
            }
        }

        # Add SMTP settings for generic version
        if self.config_type == "email":
            base_config["smtp"] = {
                "server": "",
                "port": 587
            }

        return base_config

    def load_config(self) -> Optional[Dict[str, Any]]:
        """
        Load configuration from file

        Returns:
            Configuration dictionary if file exists, None otherwise
        """
        if not self.config_file.exists():
            return None

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Validate version (optional, for future compatibility)
            if "version" not in config:
                config["version"] = self.CONFIG_VERSION

            return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config file: {e}")
            return None

    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to file

        Args:
            config: Configuration dictionary to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Add version if not present
            if "version" not in config:
                config["version"] = self.CONFIG_VERSION

            # Save to file with pretty formatting
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            # Set file permissions to user-only (for security)
            os.chmod(self.config_file, 0o600)

            return True
        except (IOError, OSError) as e:
            print(f"Error saving config file: {e}")
            return False

    def config_exists(self) -> bool:
        """
        Check if configuration file exists

        Returns:
            True if config file exists, False otherwise
        """
        return self.config_file.exists()

    def get_config_path(self) -> str:
        """
        Get the full path to the configuration file

        Returns:
            String path to config file
        """
        return str(self.config_file)

    def delete_config(self) -> bool:
        """
        Delete the configuration file

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except OSError as e:
            print(f"Error deleting config file: {e}")
            return False

    def merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge loaded config with defaults to handle missing keys

        Args:
            config: Loaded configuration dictionary

        Returns:
            Merged configuration with all required keys
        """
        default_config = self.get_default_config()

        # Deep merge function
        def deep_merge(base: dict, updates: dict) -> dict:
            result = base.copy()
            for key, value in updates.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        return deep_merge(default_config, config)


# Convenience functions for quick access

def load_email_config() -> Optional[Dict[str, Any]]:
    """Load configuration for generic email sender"""
    manager = ConfigManager("email")
    return manager.load_config()


def save_email_config(config: Dict[str, Any]) -> bool:
    """Save configuration for generic email sender"""
    manager = ConfigManager("email")
    return manager.save_config(config)


def load_gmail_config() -> Optional[Dict[str, Any]]:
    """Load configuration for Gmail sender"""
    manager = ConfigManager("gmail")
    return manager.load_config()


def save_gmail_config(config: Dict[str, Any]) -> bool:
    """Save configuration for Gmail sender"""
    manager = ConfigManager("gmail")
    return manager.save_config(config)
