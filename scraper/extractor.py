"""
extractor.py — Send a screenshot to Claude Vision and extract Q&A as JSON.

Verified API pattern (anthropic SDK 0.86+):
  client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from env
  response = client.messages.create(...)
  text = response.content[0].text         # always [0].text
"""

import anthropic
import base64
import json
from pathlib import Path


# Cheapest Claude model that supports vision
MODEL = "claude-haiku-4-5-20251001"

EXTRACTION_PROMPT = """Look at this screenshot carefully. Extract ALL questions and their answers that appear in the image.

For each question, determine whether it is a plain question or a multiple-choice question:
- Plain question: has a single direct answer.
- Multiple-choice question: has labelled answer options (e.g. A, B, C, D or 1, 2, 3, 4).

Return ONLY valid JSON in this exact format, no markdown, no explanation:
{
  "questions_and_answers": [
    {
      "question": "...",
      "answer": "...",
      "options": null
    },
    {
      "question": "...",
      "answer": "B",
      "options": [
        "A. first option",
        "B. second option",
        "C. third option",
        "D. fourth option"
      ]
    }
  ],
  "source_description": "brief description of what the screenshot shows"
}

Rules:
- "answer": the selected, highlighted, or correct answer if visible; otherwise null.
- "options": list of ALL labelled choices as strings (include the label, e.g. "A. text"); null if not multiple choice.
- If no clear questions/answers are found, return: {"questions_and_answers": [], "source_description": "..."}"""


def extract_qa(image_path: str) -> dict:
    """Send screenshot to Claude Vision and return structured Q&A.

    Args:
        image_path: Absolute path to a PNG screenshot.

    Returns:
        Dict with "questions_and_answers" (list) and "source_description" (str).
        On API error:  includes "api_error" key.
        On parse fail: includes "raw_text" and "parse_error": True.
    """
    path = Path(image_path)
    if not path.exists():
        return {
            "questions_and_answers": [],
            "source_description": "",
            "api_error": f"Image not found: {image_path}",
        }

    # Encode image to base64
    with open(path, "rb") as f:
        img_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    # Call Claude Vision API
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": EXTRACTION_PROMPT,
                        },
                    ],
                }
            ],
        )
    except anthropic.BadRequestError as e:
        msg = str(e)
        if "credit balance" in msg.lower():
            print("ERROR: Anthropic account has no credits.")
            print("  -> Add credits at: https://console.anthropic.com/settings/billing")
        return {"questions_and_answers": [], "source_description": "", "api_error": msg}
    except anthropic.APIError as e:
        return {"questions_and_answers": [], "source_description": "", "api_error": str(e)}

    response_text = response.content[0].text  # always [0].text, per SDK docs

    # Parse JSON response — graceful fallback on failure
    try:
        result = json.loads(response_text)
        result.setdefault("questions_and_answers", [])
        result.setdefault("source_description", "")
        return result
    except json.JSONDecodeError:
        return {
            "questions_and_answers": [],
            "raw_text": response_text,
            "parse_error": True,
        }
