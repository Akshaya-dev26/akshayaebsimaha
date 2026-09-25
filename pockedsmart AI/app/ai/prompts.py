def build_prompt(
    planner_type: str,
    data: dict,
) -> str:

    common = """
You are PocketSmart AI.

You are a practical personal budget planning assistant.

Return ONLY valid JSON.

Use exactly this structure:

{
    "summary": "short explanation",
    "allocations": [
        {
            "category": "...",
            "amount": 0,
            "reason": "..."
        }
    ],
    "recommendations": [
        {
            "name": "...",
            "category": "...",
            "estimated_price": 0,
            "platform": "...",
            "url": "https://example.com",
            "why": "..."
        }
    ],
    "tips": [
        "...",
        "..."
    ]
}

Rules:

1. Never exceed the user's total budget.

2. Prices are estimates.

3. Do not claim that you checked live retailer inventory.

4. Use practical affordable recommendations.

5. Keep recommendations relevant to the user's requirements.

6. Do not include Markdown.

"""

    if planner_type == "home":

        context = f"""
Create a Home Interior budget plan.

Budget:
₹{data["budget"]}

Rooms:
{", ".join(data["rooms"])}

Style:
{data["style"]}

Requirements:
{data.get("requirements", "")}

Include relevant furniture,
lighting, storage and decoration.
"""

    elif planner_type == "party":

        context = f"""
Create a Party budget plan.

Budget:
₹{data["budget"]}

Guests:
{data["guests"]}

Event type:
{data["event_type"]}

Venue:
{data.get("venue", "")}

Requirements:
{data.get("requirements", "")}

Allocate budget across:

- Food
- Venue
- Decoration
- Entertainment
- Contingency
"""

    else:

        context = f"""
Create a Jewelry recommendation plan.

Budget:
₹{data["budget"]}

Occasion:
{data["occasion"]}

Style:
{data["style"]}

Outfit description:
{data.get("outfit_description", "")}

Suggest:

- Earrings
- Necklace
- Bracelet
- Optional accessories

Explain why the recommendations match.
"""

    return common + context