#!/usr/bin/env python3
"""
Configure slow models for Smart Widgets with Ilm.
This script manages the configuration for using slow/cost-optimized models.
"""

import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path(".cursor")
CONFIG_FILE = CONFIG_DIR / "smart-widgets-config.json"

# Default slow model configuration
SLOW_MODEL_CONFIG = {
    "smartWidgets": {
        "enabled": True,
        "native": True,
        "ilm": {
            "enabled": True,
            "available": True,
            "modelType": "slow",
            "modelConfig": {
                "useSlowModels": True,
                "modelSpeed": "slow",
                "costOptimized": True,
                "timeout": 30000,
                "retryAttempts": 3,
                "modelOptions": {
                    "preferCheaper": True,
                    "allowLongerWait": True,
                    "batchProcessing": True
                }
            }
        },
        "settings": {
            "autoEnable": True,
            "fallbackToFast": False,
            "preferSlowModels": True
        }
    }
}


def load_config():
    """Load existing configuration or return default."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON in config file: {e}")
            return SLOW_MODEL_CONFIG.copy()
    return SLOW_MODEL_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Configuration saved to: {CONFIG_FILE}")


def update_model_config(config, **kwargs):
    """Update model configuration with provided parameters."""
    ilm_config = config.setdefault("smartWidgets", {}).setdefault("ilm", {})
    model_config = ilm_config.setdefault("modelConfig", {})
    
    for key, value in kwargs.items():
        if key == "timeout":
            model_config["timeout"] = int(value)
        elif key == "retryAttempts":
            model_config["retryAttempts"] = int(value)
        elif key == "modelSpeed":
            model_config["modelSpeed"] = value
        elif key == "costOptimized":
            model_config["costOptimized"] = bool(value)
        elif key == "useSlowModels":
            model_config["useSlowModels"] = bool(value)
    
    return config


def main():
    """Main function to configure slow models."""
    print("🔧 Configuring Smart Widgets with Ilm (Slow Models)")
    print("=" * 60)
    
    # Load existing config
    config = load_config()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Custom configuration via command line
        for arg in sys.argv[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                update_model_config(config, **{key: value})
    else:
        # Use default slow model configuration
        config = SLOW_MODEL_CONFIG.copy()
    
    # Ensure Ilm is enabled
    config.setdefault("smartWidgets", {}).setdefault("ilm", {})["enabled"] = True
    config.setdefault("smartWidgets", {}).setdefault("ilm", {})["available"] = True
    config.setdefault("smartWidgets", {}).setdefault("ilm", {})["modelType"] = "slow"
    
    # Save configuration
    save_config(config)
    
    # Display summary
    print("\n📋 Configuration Summary:")
    print(f"  Smart Widgets: {'✅ Enabled' if config['smartWidgets']['enabled'] else '❌ Disabled'}")
    print(f"  Native Mode: {'✅ Enabled' if config['smartWidgets']['native'] else '❌ Disabled'}")
    print(f"  Ilm Enabled: {'✅ Yes' if config['smartWidgets']['ilm']['enabled'] else '❌ No'}")
    print(f"  Ilm Available: {'✅ Yes' if config['smartWidgets']['ilm']['available'] else '❌ No'}")
    print(f"  Model Type: {config['smartWidgets']['ilm']['modelType']}")
    print(f"  Use Slow Models: {'✅ Yes' if config['smartWidgets']['ilm']['modelConfig']['useSlowModels'] else '❌ No'}")
    print(f"  Cost Optimized: {'✅ Yes' if config['smartWidgets']['ilm']['modelConfig']['costOptimized'] else '❌ No'}")
    print(f"  Timeout: {config['smartWidgets']['ilm']['modelConfig']['timeout']}ms")
    print(f"  Retry Attempts: {config['smartWidgets']['ilm']['modelConfig']['retryAttempts']}")
    
    print("\n✨ Configuration complete!")
    print("\nTo apply these settings, run:")
    print("  source .cursor/smart-widgets.env")
    print("\nOr use the enable script:")
    print("  bash scripts/enable-smart-widgets-ilm.sh")


if __name__ == "__main__":
    main()
