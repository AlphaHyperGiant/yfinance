/**
 * TypeScript definitions for Clip.js API
 */

declare class ClipAPI {
    isSupported: boolean;
    fallbackEnabled: boolean;

    constructor();

    /**
     * Check if Clipboard API is supported
     */
    checkSupport(): boolean;

    /**
     * Copy text to clipboard
     * @param text - Text to copy
     * @returns Promise resolving to success status
     */
    copy(text: string): Promise<boolean>;

    /**
     * Paste text from clipboard
     * @returns Promise resolving to clipboard text content
     */
    paste(): Promise<string>;

    /**
     * Copy data as JSON to clipboard
     * @param data - Data to copy as JSON
     * @param pretty - Pretty print JSON (default: false)
     * @returns Promise resolving to success status
     */
    copyJSON(data: any, pretty?: boolean): Promise<boolean>;

    /**
     * Paste JSON from clipboard
     * @returns Promise resolving to parsed JSON data
     */
    pasteJSON(): Promise<any>;

    /**
     * Copy HTML content to clipboard
     * @param html - HTML content
     * @param plainText - Plain text fallback
     * @returns Promise resolving to success status
     */
    copyHTML(html: string, plainText?: string): Promise<boolean>;

    /**
     * Check clipboard permissions
     * @returns Promise resolving to permission status
     */
    checkPermissions(): Promise<'granted' | 'denied' | 'prompt'>;

    /**
     * Request clipboard permissions
     * @returns Promise resolving to permission granted status
     */
    requestPermissions(): Promise<boolean>;

    /**
     * Enable or disable fallback methods
     * @param enabled - Enable fallback
     */
    setFallback(enabled: boolean): void;
}

declare const clip: ClipAPI;

export default ClipAPI;
export { clip, ClipAPI };
