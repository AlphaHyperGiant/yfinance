# Antigravity Coder

This is a native web application that provides an online coding environment with instance management and traffic phasing capabilities.

## Features

1.  **Online Coder**: Write and execute Python code directly in the browser.
2.  **Instance Management**: Deploy new versions of your code as separate instances.
3.  **Phase in Shift**: Gradually shift traffic from the stable version to the new candidate version using a percentage slider.
4.  **Rollback**: Quickly revert to any previous version.
5.  **Antigravity Mode**: A "Google Antigravity" inspired visual mode.

## How to Run

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open `http://localhost:5000` in your browser.

## usage

- **Code Editor**: Type your Python code in the text area.
- **Deploy**: Click "Deploy as New Instance" to save the current code as a new version (e.g., v2, v3).
- **Phase Shift**: Use the slider to control the probability (0-100%) that the "Execute" button runs the *New Candidate* instead of the *Current Stable*.
- **Execute**: Runs the code. The output shows which version was executed based on the phase shift setting.
- **Rollback**: Click "Rollback To" in the history list to make a previous version the "Current Stable" and reset phase shift to 0.
