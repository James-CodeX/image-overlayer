# Image Overlay API

A Python FastAPI application for overlaying text and logos on background images. Perfect for creating quote images, social media posts, and branded content.

## Features

- 🎨 Overlay custom text on any background image
- 🖼️ Add logos with customizable position and opacity
- 🎯 Flexible text positioning (center, corners, or custom coordinates)
- 🌈 Full RGBA color control for text
- 📏 Automatic text wrapping
- 🔧 RESTful API for easy integration
- 🌐 Web interface included for testing
- 📱 CORS enabled for browser access

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### 3. Use the Web Interface

Open `index.html` in your browser to use the visual interface for creating images.

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Usage Examples

### Web Interface

Simply open `index.html` in your browser:

1. Upload a background image
2. Enter your text
3. Optionally upload a logo
4. Customize colors, sizes, and positions
5. Click "Generate Image"
6. Download your result

### Using cURL

```bash
curl -X POST "http://localhost:8000/overlay" \
  -F "background=@background.jpg" \
  -F "text=Your quote text here" \
  -F "logo=@logo.png" \
  -F "text_size=50" \
  -F "text_color=50,50,50,255" \
  -F "logo_position=bottom-right" \
  --output result.png
```

### Using Python

```python
import requests

url = "http://localhost:8000/overlay"

files = {
    'background': open('background.jpg', 'rb'),
    'logo': open('logo.png', 'rb')
}

data = {
    'text': 'The secret to wealth is simple...',
    'text_size': 45,
    'text_color': '60,60,60,255',
    'text_position': 'center',
    'logo_position': 'bottom-right',
    'logo_size': '100,100',
    'max_text_width': 50
}

response = requests.post(url, files=files, data=data)

with open('output.png', 'wb') as f:
    f.write(response.content)
```

### Using JavaScript

```javascript
const formData = new FormData();
formData.append("background", backgroundFile);
formData.append("text", "Your quote here");
formData.append("logo", logoFile);
formData.append("text_size", "50");
formData.append("logo_position", "bottom-right");

fetch("http://localhost:8000/overlay", {
  method: "POST",
  body: formData,
})
  .then((response) => response.blob())
  .then((blob) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "quote.png";
    a.click();
  });
```

## API Parameters

| Parameter        | Type    | Required | Default        | Description                                                                          |
| ---------------- | ------- | -------- | -------------- | ------------------------------------------------------------------------------------ |
| `background`     | File    | Yes      | -              | Background image file                                                                |
| `text`           | String  | Yes      | -              | Text to overlay                                                                      |
| `logo`           | File    | No       | -              | Logo image file                                                                      |
| `text_position`  | String  | No       | "center"       | Position: "center", "top-left", "top-right", "bottom-left", "bottom-right", or "x,y" |
| `text_color`     | String  | No       | "0,0,0,255"    | RGBA color as "R,G,B,A"                                                              |
| `text_size`      | Integer | No       | 40             | Font size in pixels                                                                  |
| `max_text_width` | Integer | No       | None           | Maximum characters per line for word wrapping                                        |
| `logo_position`  | String  | No       | "bottom-right" | Logo position (same format as text_position)                                         |
| `logo_size`      | String  | No       | None           | Logo dimensions as "width,height"                                                    |
| `logo_opacity`   | Integer | No       | 255            | Logo opacity from 0-255                                                              |
| `output_format`  | String  | No       | "PNG"          | Output format: "PNG" or "JPEG"                                                       |

## Project Structure

```
image-overlayer/
├── app.py              # FastAPI application
├── image_processor.py  # Core image processing logic
├── index.html          # Web interface for testing
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Pillow (PIL)
- python-multipart

## License

MIT License - feel free to use this in your projects!
