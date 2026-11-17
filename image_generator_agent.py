import os
import re
import json
import time
import requests

from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

if not POLLINATIONS_API_KEY:
    raise RuntimeError("POLLINATIONS_API_KEY is missing from .env")

IMAGE_API_URL = "https://gen.pollinations.ai/image"

IMAGE_MODEL = "black-forest-labs/flux.1-schnell"

IMAGE_FOLDER = Path("generated_images")
IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)    

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    max_retries=2
)

def create_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:70]


def analyze_report_sections(report: str, max_images: int = 5) -> list:
    """
    Analyzes the research report and identifies sections
    that would benefit from educational illustrations.
    The number of images is decided dynamically by the LLM,
    subject to max_images.
    """
    prompt = f"""
You are an expert scientific research visual planner.

Analyze the following research report.

Your task is to identify the sections that would benefit
from an educational illustration, scientific diagram,
anatomical diagram, process visualization, or architecture diagram.

IMPORTANT RULES:

1. Do not generate images for every section automatically.
2. Select only sections where a visual genuinely improves understanding.
3. Identify the exact section heading from the report.
4. Create a detailed image generation prompt for each selected section.
5. Images must be educational, relevant, and scientifically accurate.
6. Avoid decorative or unrelated images.
7. Do not ask the image model to write labels or paragraphs inside images.
8. Prefer clean diagrams, realistic scientific illustrations,
   and clear visual compositions.
9. Do not generate multiple nearly identical images.
10. Select at most {max_images} images.

Return ONLY valid JSON in this format:

{{
    "images": [
        {{
            "section_heading": "Exact heading from the report",
            "image_prompt": "Detailed image-generation prompt",
            "caption": "Short figure caption"
        }}
    ]
}}

If no section needs an image, return:

{{
    "images": []
}}

RESEARCH REPORT:
{report[:18000]}
"""
    response = llm.invoke(prompt)
    content = response.content
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    # Remove possible Markdown code fences.
    content = re.sub(r"```(?:json)?", "", content).replace("```", "").strip()
    # Extract JSON in case the LLM adds introductory text.
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("The section analyzer did not return valid JSON.")
    data = json.loads(content[start:end + 1])
    images = data.get("images", [])
    if not isinstance(images, list):
        raise ValueError("Invalid image plan returned by the LLM.")
    return images[:max_images]



def generate_image(image_prompt: str, output_path: Path) -> str:
    """
    Sends the image prompt to Pollinations AI and saves
    the generated image locally.
    """
    encoded_prompt = quote(image_prompt, safe="")
    image_url = f"{IMAGE_API_URL}/{encoded_prompt}"
    headers = {
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}"
    }
    params = {
        "model": IMAGE_MODEL,
        "width": 1024,
        "height": 768,
        "nologo": "true"
    }
    response = requests.get(
        image_url,
        headers=headers,
        params=params,
        timeout=180
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/"):
        raise ValueError(
            f"Image API returned unexpected content type: {content_type}"
        )
    if not response.content:
        raise ValueError("The image API returned an empty response.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return str(output_path)



def image_generator_agent(
    report: str,
    max_images: int = 5
) -> list:
    """
    Main Image Generator Agent.
    1. Analyzes the research report.
    2. Identifies suitable sections.
    3. Generates prompts.
    4. Generates images.
    5. Saves images locally.
    6. Returns image metadata for frontend integration.
    """
    if not report or not report.strip():
        raise ValueError("Research report cannot be empty.")
    print("\n[IMAGE AGENT] Analyzing research report...")
    image_plans = analyze_report_sections(
        report=report,
        max_images=max_images
    )
    if not image_plans:
        print("[IMAGE AGENT] No sections require illustrations.")
        return []
    print(f"[IMAGE AGENT] Planned {len(image_plans)} image(s).")
    generated_images = []
    for index, plan in enumerate(image_plans, start=1):
        heading = plan.get("section_heading", "").strip()
        prompt = plan.get("image_prompt", "").strip()
        caption = plan.get("caption", "").strip()
        if not heading or not prompt:
            print(f"[IMAGE AGENT] Skipping invalid plan {index}.")
            continue
        filename = (
            f"{index:02d}_"
            f"{create_slug(heading) or 'research_image'}.jpg"
        )
        output_path = IMAGE_FOLDER / filename
        print(f"\n[IMAGE AGENT] Generating image {index}")
        print(f"Section: {heading}")
        try:
            image_path = generate_image(
                image_prompt=prompt,
                output_path=output_path
            )
            generated_images.append({
                "section_heading": heading,
                "image_prompt": prompt,
                "caption": caption,
                "image_path": image_path,
                "filename": filename,
                "status": "success"
            })
            print(f"[IMAGE AGENT] Saved: {image_path}")
        except Exception as error:
            print(
                f"[IMAGE AGENT] Failed for '{heading}': {error}"
            )
            generated_images.append({
                "section_heading": heading,
                "image_prompt": prompt,
                "caption": caption,
                "image_path": None,
                "filename": filename,
                "status": "failed",
                "error": str(error)
            })
        # Small pause between image requests.
        if index < len(image_plans):
            time.sleep(2)
    print(
        f"\n[IMAGE AGENT] Completed. "
        f"{sum(i['status'] == 'success' for i in generated_images)} "
        f"of {len(image_plans)} images generated."
    )
    return generated_images

# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------
if __name__ == "__main__":
    sample_report = """
    # Human Male Reproduction

    ## 1. Male Reproductive System

    The male reproductive system consists of the testes,
    epididymis, vas deferens, seminal vesicles and prostate gland.

    ## 2. Spermatogenesis

    Spermatogenesis is the process of sperm-cell development
    that takes place inside the seminiferous tubules.

    ## 3. Hormonal Regulation

    The hypothalamus and pituitary gland regulate male
    reproductive functions through hormonal signaling.
    """
    results = image_generator_agent(
        report=sample_report,
        max_images=5
    )
    print("\nGENERATED IMAGE DETAILS")
    for item in results:
        print(json.dumps(item, indent=4))    