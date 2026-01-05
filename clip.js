/**
 * Clip.js API - Clipboard Operations Library
 * Provides a simple and consistent API for clipboard operations
 */

class ClipAPI {
    constructor() {
        this.isSupported = this.checkSupport();
        this.fallbackEnabled = true;
    }

    /**
     * Check if Clipboard API is supported
     * @returns {boolean} True if supported
     */
    checkSupport() {
        return !!(
            navigator.clipboard ||
            (document.execCommand && document.queryCommandSupported('copy'))
        );
    }

    /**
     * Copy text to clipboard
     * @param {string} text - Text to copy
     * @returns {Promise<boolean>} Success status
     */
    async copy(text) {
        if (!text) {
            throw new Error('ClipAPI.copy: Text parameter is required');
        }

        try {
            // Modern Clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
                return true;
            }

            // Fallback for older browsers
            if (this.fallbackEnabled) {
                return this.fallbackCopy(text);
            }

            throw new Error('Clipboard API not supported and fallback disabled');
        } catch (error) {
            console.error('ClipAPI.copy error:', error);
            throw error;
        }
    }

    /**
     * Paste text from clipboard
     * @returns {Promise<string>} Clipboard text content
     */
    async paste() {
        try {
            // Modern Clipboard API
            if (navigator.clipboard && navigator.clipboard.readText) {
                const text = await navigator.clipboard.readText();
                return text;
            }

            // Fallback - requires user interaction
            if (this.fallbackEnabled) {
                return this.fallbackPaste();
            }

            throw new Error('Clipboard API not supported and fallback disabled');
        } catch (error) {
            console.error('ClipAPI.paste error:', error);
            throw error;
        }
    }

    /**
     * Copy data as JSON to clipboard
     * @param {any} data - Data to copy as JSON
     * @param {boolean} pretty - Pretty print JSON
     * @returns {Promise<boolean>} Success status
     */
    async copyJSON(data, pretty = false) {
        try {
            const jsonString = pretty 
                ? JSON.stringify(data, null, 2)
                : JSON.stringify(data);
            return await this.copy(jsonString);
        } catch (error) {
            console.error('ClipAPI.copyJSON error:', error);
            throw error;
        }
    }

    /**
     * Paste JSON from clipboard
     * @returns {Promise<any>} Parsed JSON data
     */
    async pasteJSON() {
        try {
            const text = await this.paste();
            return JSON.parse(text);
        } catch (error) {
            console.error('ClipAPI.pasteJSON error:', error);
            throw new Error('Failed to parse clipboard content as JSON');
        }
    }

    /**
     * Copy HTML content to clipboard
     * @param {string} html - HTML content
     * @param {string} plainText - Plain text fallback
     * @returns {Promise<boolean>} Success status
     */
    async copyHTML(html, plainText = '') {
        try {
            if (navigator.clipboard && navigator.clipboard.write) {
                const clipboardItem = new ClipboardItem({
                    'text/html': new Blob([html], { type: 'text/html' }),
                    'text/plain': new Blob([plainText || html], { type: 'text/plain' })
                });
                await navigator.clipboard.write([clipboardItem]);
                return true;
            }

            // Fallback to plain text
            return await this.copy(plainText || html);
        } catch (error) {
            console.error('ClipAPI.copyHTML error:', error);
            throw error;
        }
    }

    /**
     * Fallback copy method for older browsers
     * @param {string} text - Text to copy
     * @returns {boolean} Success status
     */
    fallbackCopy(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);
            return successful;
        } catch (error) {
            document.body.removeChild(textArea);
            console.error('Fallback copy failed:', error);
            return false;
        }
    }

    /**
     * Fallback paste method (requires user interaction)
     * @returns {Promise<string>} Clipboard text
     */
    fallbackPaste() {
        return new Promise((resolve, reject) => {
            const textArea = document.createElement('textarea');
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();

            // Trigger paste event
            setTimeout(() => {
                try {
                    const text = textArea.value;
                    document.body.removeChild(textArea);
                    resolve(text);
                } catch (error) {
                    document.body.removeChild(textArea);
                    reject(error);
                }
            }, 100);
        });
    }

    /**
     * Check clipboard permissions
     * @returns {Promise<string>} Permission status ('granted', 'denied', 'prompt')
     */
    async checkPermissions() {
        if (navigator.permissions && navigator.permissions.query) {
            try {
                const result = await navigator.permissions.query({ name: 'clipboard-read' });
                return result.state;
            } catch (error) {
                // Fallback for browsers that don't support clipboard permissions
                return 'prompt';
            }
        }
        return 'prompt';
    }

    /**
     * Request clipboard permissions
     * @returns {Promise<boolean>} Permission granted
     */
    async requestPermissions() {
        try {
            // Try to read clipboard to trigger permission prompt
            await navigator.clipboard.readText();
            return true;
        } catch (error) {
            if (error.name === 'NotAllowedError') {
                return false;
            }
            throw error;
        }
    }

    /**
     * Enable or disable fallback methods
     * @param {boolean} enabled - Enable fallback
     */
    setFallback(enabled) {
        this.fallbackEnabled = enabled;
    }
}

// Create singleton instance
const clip = new ClipAPI();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    // CommonJS
    module.exports = ClipAPI;
    module.exports.clip = clip;
} else if (typeof define === 'function' && define.amd) {
    // AMD
    define([], function() {
        return ClipAPI;
    });
} else {
    // Browser global
    window.ClipAPI = ClipAPI;
    window.clip = clip;
}

// ES6 Module export (if supported)
if (typeof window !== 'undefined') {
    window.ClipAPI = ClipAPI;
    window.clip = clip;
}
