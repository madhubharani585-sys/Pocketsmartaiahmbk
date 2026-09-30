"""Gemini integration: builds prompts, calls the model, parses and cleans JSON."""
import json
import os
import re
from urllib.parse import quote_plus

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
_client = None

SYSTEM = """You are PocketSmart AI, a careful budget and shopping planner for Indian users.
All prices are in Indian Rupees (INR). Never exceed the user's total budget.
Recommend realistic, typical products/services available on the requested platforms.
Do NOT invent URLs. Give a short search_query for each item instead.
Respond ONLY with JSON matching this shape:
{
 "summary": "2-3 sentence overview",
 "allocation": [{"category": str, "amount": number, "note": str}],
 "items": [{"category": str, "name": str, "platform": str, "est_price": number,
            "why": str, "search_query": str}],
 "tips": [str]
}
allocation amounts must sum to at most the total budget; est_price is per line total."""

# Platform -> search URL template. Links are built here so they never hallucinate.
PLATFORM_URLS = {
    "amazon": "https://www.amazon.in/s?k={q}",
    "flipkart": "https://www.flipkart.com/search?q={q}",
    "ikea": "https://www.ikea.com/in/en/search/?q={q}",
    "swiggy": "https://www.swiggy.com/search?query={q}",
    "zomato": "https://www.zomato.com/search?q={q}",
    "oyo": "https://www.oyorooms.com/search?query={q}",
}


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key or key == "your_api_key_here":
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to backend/.env")
        _client = genai.Client(api_key=key)
    return _client


def _extract_json(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise ValueError("AI returned an unreadable response. Please try again.")
        return json.loads(match.group(0))


def _clean(data, budget):
    data.setdefault("summary", "")
    data.setdefault("allocation", [])
    data.setdefault("items", [])
    data.setdefault("tips", [])
    for item in data["items"]:
        platform = str(item.get("platform", "")).strip()
        query = quote_plus(item.get("search_query") or item.get("name", ""))
        tpl = PLATFORM_URLS.get(platform.lower(), PLATFORM_URLS["amazon"])
        item["url"] = tpl.format(q=query)
        try:
            item["est_price"] = float(item.get("est_price", 0))
        except (TypeError, ValueError):
            item["est_price"] = 0
    data["total_estimated"] = round(sum(i["est_price"] for i in data["items"]), 2)
    data["budget"] = budget
    return data


def generate_plan(user_prompt, budget, image=None):
    """image: optional (bytes, mime_type) tuple."""
    contents = [user_prompt]
    if image:
        contents.insert(0, types.Part.from_bytes(data=image[0], mime_type=image[1]))
    response = _get_client().models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            response_mime_type="application/json",
            temperature=0.6,
        ),
    )
    return _clean(_extract_json(response.text or ""), budget)


# ---------- Prompt builders (one per planner) ----------
def home_prompt(budget, items):
    lines = "\n".join(f"- {i['room']}: {i['qty']} x {i['item']}" for i in items)
    return (
        f"Plan a HOME INTERIOR purchase. Total budget: INR {budget}.\n"
        f"Needed items:\n{lines}\n"
        "Platforms: IKEA, Amazon, Flipkart. Balance functionality, style and price. "
        "Allocate budget per room in 'allocation' and give one or more items per need."
    )


def party_prompt(budget, guests, event, venue, city):
    return (
        f"Plan a {event.upper()} PARTY. Total budget: INR {budget}. Guests: {guests}. "
        f"Venue: {venue}. City: {city or 'not specified'}.\n"
        "Split the budget across Catering, Decoration and Entertainment (and Stay via OYO "
        "only if the venue/guests need accommodation). Use Swiggy and Zomato for food, "
        "Amazon/Flipkart for decor and props. Tailor to the event type."
    )


def jewelry_prompt(budget, occasion, style, notes, has_image):
    img = ("An outfit photo is attached: match jewelry to its colors and neckline. "
           if has_image else "")
    return (
        f"Recommend JEWELRY for a {occasion}. Total budget: INR {budget}. "
        f"Style preference: {style}. Extra notes: {notes or 'none'}. {img}"
        "Platforms: Amazon and Flipkart. Suggest a coordinated set (necklace, earrings, "
        "bangles, etc.) and explain color/style matching in 'why'."
    )
