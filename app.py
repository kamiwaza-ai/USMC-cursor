import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Load data once at startup
with open("meu_logistics_data.csv") as f:
    DATA = f.read()

SYSTEM_PROMPT = f"""You are a logistics analyst for Marine Expeditionary Unit (MEU) operations.

Use the data below to answer questions. Always reference specific numbers with units.

--- MEU LOGISTICS DATA ---
{DATA}
--- END DATA ---
"""

def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

gr.ChatInterface(
    chat,
    title="MEU Logistics Assistant",
    description="Ask questions about Marine Expeditionary Unit logistics data.",
    examples=[
        "What units make up the MEU?",
        "What's the daily fuel consumption during offensive operations?",
        "Compare Guam and Darwin port capacities",
        "What aircraft does the ACE have?"
    ]
).launch()
