# Smart Widgets Native with Ilm (Slow Models)

This document describes the process for enabling and configuring Smart Widgets with Ilm support using slow models.

## Overview

Smart Widgets Native with Ilm provides an intelligent widget system that uses slower, cost-optimized models for processing. This configuration is ideal for scenarios where cost optimization is prioritized over speed.

## Features

- ✅ Native Smart Widgets support
- ✅ Ilm integration available
- ✅ Slow model configuration for cost optimization
- ✅ Configurable timeout and retry settings
- ✅ Automated workflow support

## Quick Start

### Option 1: Using the Shell Script

```bash
# Make the script executable
chmod +x scripts/enable-smart-widgets-ilm.sh

# Run the script
bash scripts/enable-smart-widgets-ilm.sh

# Source the environment variables
source .cursor/smart-widgets.env
```

### Option 2: Using the Python Script

```bash
# Configure with default slow model settings
python3 scripts/configure-slow-models.py

# Or customize settings
python3 scripts/configure-slow-models.py timeout=60000 retryAttempts=5
```

### Option 3: Manual Configuration

1. Ensure the `.cursor` directory exists:
   ```bash
   mkdir -p .cursor
   ```

2. Create or update `.cursor/smart-widgets-config.json`:
   ```json
   {
     "smartWidgets": {
       "enabled": true,
       "native": true,
       "ilm": {
         "enabled": true,
         "available": true,
         "modelType": "slow",
         "modelConfig": {
           "useSlowModels": true,
           "modelSpeed": "slow",
           "costOptimized": true,
           "timeout": 30000,
           "retryAttempts": 3
         }
       },
       "settings": {
         "autoEnable": true,
         "fallbackToFast": false,
         "preferSlowModels": true
       }
     }
   }
   ```

3. Source the environment file:
   ```bash
   source .cursor/smart-widgets.env
   ```

## Configuration Options

### Model Configuration

- `useSlowModels`: Enable slow model usage (default: `true`)
- `modelSpeed`: Model speed setting (default: `"slow"`)
- `costOptimized`: Enable cost optimization (default: `true`)
- `timeout`: Request timeout in milliseconds (default: `30000`)
- `retryAttempts`: Number of retry attempts (default: `3`)

### Smart Widgets Settings

- `enabled`: Enable Smart Widgets (default: `true`)
- `native`: Enable native mode (default: `true`)
- `autoEnable`: Automatically enable widgets (default: `true`)
- `fallbackToFast`: Fallback to fast models on failure (default: `false`)
- `preferSlowModels`: Prefer slow models over fast ones (default: `true`)

## Environment Variables

The following environment variables are set when using the enable script:

- `SMART_WIDGETS_ENABLED=true`
- `SMART_WIDGETS_NATIVE=true`
- `ILM_ENABLED=true`
- `ILM_AVAILABLE=true`
- `ILM_MODEL_TYPE=slow`
- `ILM_USE_SLOW_MODELS=true`
- `ILM_COST_OPTIMIZED=true`

## GitHub Actions Workflow

A GitHub Actions workflow is available at `.github/workflows/smart-widgets-ilm.yml` that can be triggered manually or automatically on configuration changes.

To trigger manually:
1. Go to Actions tab in GitHub
2. Select "Smart Widgets Ilm Configuration"
3. Click "Run workflow"
4. Configure options and run

## Troubleshooting

### Configuration Not Applied

If settings aren't being applied:

1. Verify the configuration file exists:
   ```bash
   cat .cursor/smart-widgets-config.json
   ```

2. Validate JSON syntax:
   ```bash
   python3 -m json.tool .cursor/smart-widgets-config.json
   ```

3. Ensure environment variables are set:
   ```bash
   source .cursor/smart-widgets.env
   env | grep ILM
   ```

### Slow Model Timeouts

If you're experiencing timeouts with slow models:

1. Increase the timeout value:
   ```python
   python3 scripts/configure-slow-models.py timeout=60000
   ```

2. Increase retry attempts:
   ```python
   python3 scripts/configure-slow-models.py retryAttempts=5
   ```

## Best Practices

1. **Cost Optimization**: Use slow models for non-time-critical operations
2. **Timeout Settings**: Set appropriate timeouts based on your use case
3. **Retry Logic**: Configure retry attempts for unreliable network conditions
4. **Monitoring**: Monitor model performance and adjust settings as needed

## Files

- `.cursor/smart-widgets-config.json` - Main configuration file
- `.cursor/smart-widgets.env` - Environment variables file
- `scripts/enable-smart-widgets-ilm.sh` - Shell script for enabling
- `scripts/configure-slow-models.py` - Python script for configuration
- `.github/workflows/smart-widgets-ilm.yml` - GitHub Actions workflow

## Support

For issues or questions, please refer to the project's issue tracker or documentation.
