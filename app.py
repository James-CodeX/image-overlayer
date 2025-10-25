import utils.transport
import utils.session
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from image_processor import ImageOverlay
from typing import Optional
import json

app = FastAPI(title="Image Overlay API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "Image Overlay API",
        "endpoints": {
            "/overlay": "POST - Create image with text and logo overlay",
            "/docs": "API documentation"
        }
    }


@app.post("/overlay")
async def create_overlay(
    background: UploadFile = File(..., description="Background image"),
    text: str = Form(..., description="Text to overlay"),
    logo: Optional[UploadFile] = File(
        None, description="Logo image (optional)"),
    text_position: str = Form(
        "center", description="Text position: center, top-left, etc or x,y"),
    text_color: str = Form("0,0,0,255", description="Text color as R,G,B,A"),
    text_size: int = Form(40, description="Font size"),
    max_text_width: Optional[int] = Form(
        None, description="Max characters per line"),
    logo_position: str = Form("bottom-right", description="Logo position"),
    logo_size: Optional[str] = Form(
        None, description="Logo size as width,height"),
    logo_opacity: int = Form(255, description="Logo opacity 0-255"),
    output_format: str = Form("PNG", description="Output format: PNG or JPEG")
):
    """
    Create an image with text and optional logo overlay
    """
    # Read background image
    bg_bytes = await background.read()

    # Initialize processor
    processor = ImageOverlay(bg_bytes)

    # Parse text color
    color = tuple(map(int, text_color.split(',')))

    # Parse text position
    if ',' in text_position:
        text_pos = tuple(map(int, text_position.split(',')))
    else:
        text_pos = text_position

    # Add text
    processor.add_text(
        text=text,
        position=text_pos,
        font_size=text_size,
        color=color,
        max_width=max_text_width
    )

    # Add logo if provided
    if logo:
        logo_bytes = await logo.read()

        # Parse logo size
        logo_size_tuple = None
        if logo_size:
            logo_size_tuple = tuple(map(int, logo_size.split(',')))

        # Parse logo position
        if ',' in logo_position:
            logo_pos = tuple(map(int, logo_position.split(',')))
        else:
            logo_pos = logo_position

        processor.add_logo(
            logo_image=logo_bytes,
            position=logo_pos,
            size=logo_size_tuple,
            opacity=logo_opacity
        )

    # Get result
    result = processor.get_result(format=output_format)

    return StreamingResponse(
        result,
        media_type=f"image/{output_format.lower()}",
        headers={
            "Content-Disposition": f"attachment; filename=overlay.{output_format.lower()}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
