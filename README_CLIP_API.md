# Clip.js API

A simple and consistent JavaScript API for clipboard operations with cross-browser support.

## Features

- ✅ Modern Clipboard API support
- ✅ Fallback support for older browsers
- ✅ Copy/paste text
- ✅ Copy/paste JSON
- ✅ Copy HTML content
- ✅ Permission handling
- ✅ TypeScript definitions included
- ✅ Zero dependencies

## Installation

### Browser

```html
<script src="clip.js"></script>
```

### Node.js / ES Modules

```javascript
import ClipAPI from './clip.js';
const clip = new ClipAPI();
```

### CommonJS

```javascript
const { ClipAPI, clip } = require('./clip.js');
```

## Quick Start

```javascript
// Using the singleton instance
await clip.copy('Hello, World!');
const text = await clip.paste();

// Or create your own instance
const myClip = new ClipAPI();
await myClip.copy('Custom instance');
```

## API Reference

### `clip.copy(text)`

Copy text to clipboard.

```javascript
await clip.copy('Hello, World!');
```

**Parameters:**
- `text` (string): Text to copy

**Returns:** `Promise<boolean>` - Success status

### `clip.paste()`

Paste text from clipboard.

```javascript
const text = await clip.paste();
console.log(text);
```

**Returns:** `Promise<string>` - Clipboard text content

### `clip.copyJSON(data, pretty)`

Copy data as JSON to clipboard.

```javascript
const data = { name: 'Clip.js', version: '1.0.0' };
await clip.copyJSON(data);           // Compact JSON
await clip.copyJSON(data, true);     // Pretty printed JSON
```

**Parameters:**
- `data` (any): Data to copy as JSON
- `pretty` (boolean, optional): Pretty print JSON (default: `false`)

**Returns:** `Promise<boolean>` - Success status

### `clip.pasteJSON()`

Paste and parse JSON from clipboard.

```javascript
const data = await clip.pasteJSON();
console.log(data);
```

**Returns:** `Promise<any>` - Parsed JSON data

**Throws:** Error if clipboard content is not valid JSON

### `clip.copyHTML(html, plainText)`

Copy HTML content to clipboard.

```javascript
await clip.copyHTML('<h1>Title</h1>', 'Title');
```

**Parameters:**
- `html` (string): HTML content
- `plainText` (string, optional): Plain text fallback

**Returns:** `Promise<boolean>` - Success status

### `clip.checkPermissions()`

Check clipboard permissions.

```javascript
const status = await clip.checkPermissions();
// Returns: 'granted', 'denied', or 'prompt'
```

**Returns:** `Promise<string>` - Permission status

### `clip.requestPermissions()`

Request clipboard permissions.

```javascript
const granted = await clip.requestPermissions();
if (granted) {
    console.log('Permission granted!');
}
```

**Returns:** `Promise<boolean>` - Permission granted status

### `clip.setFallback(enabled)`

Enable or disable fallback methods.

```javascript
clip.setFallback(true);  // Enable fallback
clip.setFallback(false); // Disable fallback
```

**Parameters:**
- `enabled` (boolean): Enable fallback

### Properties

- `clip.isSupported` (boolean): Whether Clipboard API is supported
- `clip.fallbackEnabled` (boolean): Whether fallback is enabled

## Examples

### Basic Copy/Paste

```javascript
// Copy text
await clip.copy('Hello, World!');

// Paste text
const text = await clip.paste();
console.log(text); // "Hello, World!"
```

### Working with JSON

```javascript
// Copy object as JSON
const data = {
    ticker: 'AAPL',
    price: 150.25,
    volume: 1000000
};
await clip.copyJSON(data, true);

// Paste and parse JSON
const pastedData = await clip.pasteJSON();
console.log(pastedData.ticker); // "AAPL"
```

### HTML Content

```javascript
// Copy HTML with plain text fallback
await clip.copyHTML(
    '<h1>Title</h1><p>Content</p>',
    'Title\nContent'
);
```

### Error Handling

```javascript
try {
    await clip.copy('Some text');
    console.log('Copied successfully!');
} catch (error) {
    console.error('Copy failed:', error.message);
}
```

### Permission Handling

```javascript
// Check permissions
const status = await clip.checkPermissions();
if (status !== 'granted') {
    // Request permissions
    const granted = await clip.requestPermissions();
    if (!granted) {
        console.warn('Clipboard permission denied');
    }
}
```

## Browser Support

- ✅ Chrome/Edge 66+
- ✅ Firefox 63+
- ✅ Safari 13.1+
- ✅ Opera 53+
- ✅ Fallback for older browsers (using `document.execCommand`)

## Security Notes

- Clipboard API requires HTTPS (except for `localhost`)
- Some browsers require user interaction for clipboard operations
- Permissions may be required for reading clipboard content

## TypeScript

TypeScript definitions are included in `clip-api.d.ts`. Import types:

```typescript
import ClipAPI, { clip } from './clip.js';
```

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
