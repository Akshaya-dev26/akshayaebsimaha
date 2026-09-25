from urllib.parse import quote_plus

from ..ai.gemini_service import GeminiService

from ..ai.prompts import build_prompt


gemini = GeminiService()


def search_url(
    platform: str,
    query: str,
) -> str:

    q = quote_plus(query)

    urls = {

        "Amazon":
            f"https://www.amazon.in/s?k={q}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={q}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={q}",

        "Swiggy":
            "https://www.swiggy.com/",

        "Zomato":
            "https://www.zomato.com/",

        "OYO":
            "https://www.oyorooms.com/",
    }

    return urls.get(
        platform,
        f"https://www.google.com/search?q={q}",
    )


def fallback_home(data):

    budget = data["budget"]

    allocations = [

        {
            "category": "Furniture",
            "amount": round(budget * 0.40, 2),
            "reason": "Core functional furniture",
        },

        {
            "category": "Lighting",
            "amount": round(budget * 0.15, 2),
            "reason": "Comfort and ambience",
        },

        {
            "category": "Decor",
            "amount": round(budget * 0.20, 2),
            "reason": "Style and finishing",
        },

        {
            "category": "Contingency",
            "amount": round(budget * 0.25, 2),
            "reason": "Unexpected room requirements",
        },
    ]

    names = [
        "LED ceiling light",
        "Accent wall art",
        "Storage unit",
        "Curtain set",
        "Side table",
    ]

    platforms = [
        "IKEA",
        "Amazon",
        "Flipkart",
        "Amazon",
        "IKEA",
    ]

    recommendations = []

    for name, platform in zip(
        names,
        platforms,
    ):

        price = round(
            min(budget / 6, 4500),
            2,
        )

        recommendations.append({

            "name":
                f"{data['style']} {name}",

            "category":
                "Home",

            "estimated_price":
                price,

            "platform":
                platform,

            "url":
                search_url(
                    platform,
                    name,
                ),

            "why":
                f"Suitable for a {data['style']} setup.",
        })

    return {

        "summary":
            f"A practical {data['style']} plan "
            f"for {', '.join(data['rooms'])} "
            f"within ₹{budget:,.0f}.",

        "allocations":
            allocations,

        "recommendations":
            recommendations,

        "tips": [
            "Measure the room before buying furniture.",
            "Keep contingency money for delivery and installation.",
        ],
    }


def fallback_party(data):

    budget = data["budget"]

    guests = data["guests"]

    allocations = [

        {
            "category": "Food/Catering",
            "amount": round(budget * 0.45, 2),
            "reason": "Main guest-facing expense",
        },

        {
            "category": "Decoration",
            "amount": round(budget * 0.20, 2),
            "reason": "Theme and ambience",
        },

        {
            "category": "Venue",
            "amount": round(budget * 0.20, 2),
            "reason": "Space and facilities",
        },

        {
            "category": "Entertainment/Buffer",
            "amount": round(budget * 0.15, 2),
            "reason": "Activities and unexpected costs",
        },
    ]

    recommendations = [

        {
            "name": "Catering package",
            "category": "Food",
            "estimated_price": round(
                budget * 0.45,
                2,
            ),
            "platform": "Swiggy",
            "url": search_url(
                "Swiggy",
                "party catering",
            ),
            "why":
                "Useful for comparing food options.",
        },

        {
            "name": "Food and snacks",
            "category": "Food",
            "estimated_price": round(
                budget * 0.12,
                2,
            ),
            "platform": "Zomato",
            "url": search_url(
                "Zomato",
                "party food",
            ),
            "why":
                "Useful for additional food choices.",
        },

        {
            "name": "Decoration package",
            "category": "Decoration",
            "estimated_price": round(
                budget * 0.20,
                2,
            ),
            "platform": "Local/Other",
            "url": search_url(
                "Local/Other",
                "party decoration",
            ),
            "why":
                "Keeps decoration within budget.",
        },
    ]

    return {

        "summary":
            f"An {data['event_type']} plan "
            f"for {guests} guests at about "
            f"₹{budget / guests:,.0f} per guest.",

        "allocations":
            allocations,

        "recommendations":
            recommendations,

        "tips": [
            "Confirm the final headcount before ordering.",
            "Keep a small buffer for last-minute changes.",
        ],
    }


def fallback_jewelry(data):

    budget = data["budget"]

    style = data["style"]

    recommendations = [

        {
            "name": f"{style} earrings",
            "category": "Earrings",
            "estimated_price": round(
                budget * 0.25,
                2,
            ),
            "platform": "Amazon",
            "url": search_url(
                "Amazon",
                f"{style} earrings",
            ),
            "why":
                "A versatile option for the occasion.",
        },

        {
            "name": f"{style} necklace",
            "category": "Necklace",
            "estimated_price": round(
                budget * 0.45,
                2,
            ),
            "platform": "Flipkart",
            "url": search_url(
                "Flipkart",
                f"{style} necklace",
            ),
            "why":
                "Keeps the main visual focus within budget.",
        },

        {
            "name": f"{style} bracelet",
            "category": "Bracelet",
            "estimated_price": round(
                budget * 0.20,
                2,
            ),
            "platform": "Amazon",
            "url": search_url(
                "Amazon",
                f"{style} bracelet",
            ),
            "why":
                "Optional finishing piece.",
        },
    ]

    return {

        "summary":
            f"Jewelry suggestions for a "
            f"{data['occasion']} with a "
            f"{style} preference and "
            f"₹{budget:,.0f} budget.",

        "allocations": [

            {
                "category": "Primary piece",
                "amount": round(
                    budget * 0.45,
                    2,
                ),
                "reason": "Main visual focus",
            },

            {
                "category": "Earrings",
                "amount": round(
                    budget * 0.25,
                    2,
                ),
                "reason": "Frames the face",
            },

            {
                "category": "Optional accessories",
                "amount": round(
                    budget * 0.20,
                    2,
                ),
                "reason": "Adds coordination",
            },

            {
                "category": "Contingency",
                "amount": round(
                    budget * 0.10,
                    2,
                ),
                "reason": "Price variation",
            },
        ],

        "recommendations":
            recommendations,

        "tips": [
            "Match jewelry tone with the outfit's dominant colors.",
            "Image matching is a style suggestion, not an exact color guarantee.",
        ],
    }


async def get_recommendations(
    planner_type,
    data,
    image_bytes=None,
    mime_type=None,
):

    try:

        result = await gemini.generate(
            build_prompt(
                planner_type,
                data,
            ),
            image_bytes,
            mime_type,
        )

        result.setdefault(
            "allocations",
            [],
        )

        result.setdefault(
            "recommendations",
            [],
        )

        result.setdefault(
            "tips",
            [],
        )

        result.setdefault(
            "summary",
            "AI-generated budget plan.",
        )

        return result, "gemini"

    except Exception:

        if planner_type == "home":

            return (
                fallback_home(data),
                "local-fallback",
            )

        if planner_type == "party":

            return (
                fallback_party(data),
                "local-fallback",
            )

        return (
            fallback_jewelry(data),
            "local-fallback",
        )