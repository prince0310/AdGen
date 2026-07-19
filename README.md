# AdGen

AdGen is a FastAPI-based backend application that generates realistic marketing scenes from a single product image. The system analyzes the uploaded product, extracts its attributes, generates contextual scene prompts, and produces advertising images using FLUX.1 Kontext.

## Features

- Product image upload and description by user
  
  <img width="1337" height="740" alt="upload" src="https://github.com/user-attachments/assets/cb6aee9f-fac6-4bd5-a4f1-5d3ca4bb477a" />

- Product analysis using Gemini and Metadata extraction and Metadata caching 
```
{
  "product_name": "Revolution Skincare London 10% Niacinamide + 1% Zinc Blemish & Pore Refining Serum",
  "category": "Skincare Serum",
  "description": "A blemish and pore refining serum formulated with 10% Niacinamide and 1% Zinc to help clarify and smooth the skin. Vegan, cruelty-free, and fragrance-free formula.",
  "packaging": "Frosted glass bottle with a white dropper pipette featuring a metallic rose gold collar.",
  "primary_colors": [
    "White",
    "Rose Gold",
    "Frosted Clear"
  ],
  "brand_style": "Minimalist, clean, clinical-chic, and modern"
}
```
- Marketing prompt generation
  Example Prompt 
```
        prompt = f"""
            You are an expert prompt engineer for FLUX Kontext.

            The uploaded product image will be supplied separately as the reference image.
            Use the provided reference product image exactly as supplied.

            Do not modify the product itself.

            Only change the surrounding environment.

            The product has already been analyzed.

            Product Information

            Name:
            {metadata.product_name}

            Category:
            {metadata.category}

            Description:
            {metadata.description}

            Packaging:
            {metadata.packaging}

            Brand Style:
            {metadata.brand_style}

            Primary Colors:
            {", ".join(metadata.primary_colors)}

            Generate ONE FLUX Kontext prompt for EACH of these scenarios:

            {chr(10).join(f"- {scenario}" for scenario in scenarios)}

            IMPORTANT RULES

            The product image is provided separately.

            Do NOT redesign the product.

            Do NOT describe the bottle shape in detail.

            Do NOT recreate the label.

            Do NOT recreate the logo.

            Assume the product already exists exactly as desired.

            Your job is ONLY to describe:

            - environment
            - composition
            - camera angle
            - lighting
            - shadows
            - reflections
            - atmosphere
            - styling
            - props
            - background
            - depth of field

            Every prompt MUST explicitly instruct FLUX Kontext to preserve:

            - logo
            - branding
            - packaging
            - bottle
            - cap
            - colors
            - proportions
            - text
            - label placement

            The output should feel like instructions for an image editing model rather than an image generation model.

            Each prompt should , commercial-quality, and suitable for luxury product advertising.

            Return ONLY valid JSON.

            Format:

            {{
                "prompts": [
                    "...",
                    "...",
                    "..."
                ]
            }}
            """
```
  
- Scene generation using FLUX.1 Kontext

<img width="1313" height="608" alt="Screenshot 2026-07-19 102057" src="https://github.com/user-attachments/assets/9ec2ed27-d404-4b9c-82cf-2a8df5867aa0" />



## Workflow

```
Product Image
      │
      ▼
Gemini Analysis
      │
      ▼
Metadata Extraction
      │
      ▼
Prompt Generation
      │
      ▼
FLUX.1 Kontext
      │
      ▼
Generated Marketing Scenes
```

## Project Structure

```
app/
├── api/
├── core/
├── models/
├── providers/
├── services/
├── generated/
├── metadata/
├── uploads/
└── main.py
```

## Technology Stack

- FastAPI
- Python
- Gemini API
- Hugging Face Inference API
- FLUX.1 Kontext
- Pillow
- Pydantic

## Installation

Clone the repository.

```bash
git clone https://github.com/prince0310/AdGen.git
cd AdGen
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxx

HF_API_KEY=xxxxxxxxxxxxxxxxxxxxxx

GEMINI_MODEL=gemini-2.5-flash
FLUX_MODEL=black-forest-labs/FLUX.1-Kontext-dev
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## Demo 

<img width="1240" height="1818" alt="Screenshot_19-7-2026_10244_localhost" src="https://github.com/user-attachments/assets/aabe55c0-9edc-452e-926b-a16c54ad4697" />


## Future Improvements

- Batch generation
- User authentication
- Docker support
- Additional AI providers
- Cloud storage integration

## License

MIT License.
