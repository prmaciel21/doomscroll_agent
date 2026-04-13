import anthropic
import json
from analysis import analyze

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

SYSTEM_PROMPT = """You are a social media strategist analyzing Instagram Reels data 
for a client. Your job is to produce a clear, actionable report from raw analytics data.

Always structure your output with these sections:
1. Top 3 content trends right now (what topics/styles are performing best)
2. Best times to post (specific time slots with reasoning)
3. Hashtag strategy (which hashtags to use and why)
4. Content brief (concrete recommendations: what to film, how to structure it, 
   what tone to use) — written as if briefing a content creator
5. One "bold move" recommendation — something slightly contrarian or unexpected 
   that the data hints at

Be specific. Avoid generic advice. Every recommendation must be grounded in the data."""

def generate_report(days: int = 30) -> str:
    data = analyze(days=days)
    if not data:
        return "Not enough data yet. Run more scraping cycles first."
    user_message = f"""Here is the Instagram Reels analytics data for the past {days} days:
{json.dumps(data, indent=2)}

Please generate the full client report."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    return message.content[0].text