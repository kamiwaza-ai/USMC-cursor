# Product Requirements Document: MEU Logistics Chat Agent

## Overview

Build a simple web chatbot that lets users ask questions about Marine Expeditionary Unit (MEU) logistics data. Uses GPT-5.2 with the entire dataset in the prompt—no RAG, no vector databases, no complexity.

---

## Goal

Create a **working chatbot in under 30 lines of Python** using Gradio for the UI.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Gradio App                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  - Built-in chat interface                      │   │
│  │  - Handles message history automatically        │   │
│  │  - Auto-generates web UI                        │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  chat() function                                │   │
│  │  - Loads CSV data                               │   │
│  │  - Builds prompt with data                      │   │
│  │  - Calls OpenAI GPT-5.2                         │   │
│  │  - Returns response                             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   OpenAI API                            │
│  - Model: gpt-5.2                                      │
│  - System prompt contains full CSV (~85KB)             │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| UI | **Gradio** | Zero frontend code, built-in chat component |
| LLM | **OpenAI GPT-5.2** | Large context window fits entire dataset |
| Language | **Python** | That's it. Just Python. |

---

## File Structure

```
USMC-cursor/
├── app.py                 # The entire application (~25 lines)
├── meu_logistics_data.csv # MEU logistics dataset
├── requirements.txt       # gradio, openai
├── .env.example           # API key (pre-filled for users)
├── README.md              # Instructions
└── PRD.md                 # This document
```

---

## Implementation

### File: `app.py`

```python
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
    # Build messages from history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    # Call GPT-5.2
    response = client.chat.completions.create(
        model="gpt-4o",  # Change to gpt-5.2 when available
        messages=messages
    )
    return response.choices[0].message.content

# Launch the app
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
```

That's the entire application.

---

## How It Works

1. **Gradio** creates a web chat interface automatically
2. User types a question
3. `chat()` function is called with the message and conversation history
4. Function builds the prompt with MEU data + conversation history
5. Calls OpenAI API
6. Returns response to display in chat

---

## Running the App

```bash
# Install dependencies
pip install gradio openai python-dotenv

# Copy the env file (API key is pre-filled)
cp .env.example .env

# Run
python app.py
```

Gradio automatically opens a browser to `http://localhost:7860`

---

## System Prompt

The system prompt contains:
1. Role definition (logistics analyst)
2. Instructions (reference specific numbers, include units)
3. The entire CSV dataset (~85KB, ~2000 lines)

GPT-5.2's context window easily handles this.

---

## Example Interactions

**User:** What units make up the MEU?

**Assistant:** The MEU consists of 5 elements:
- **MEU-CE** (Command Element): 450 personnel
- **BLT-1/5** (Battalion Landing Team): 1,200 personnel
- **ACE-31** (Aviation Combat Element): 850 personnel
- **LCE-15** (Logistics Combat Element): 600 personnel
- **ARG-1** (Amphibious Ready Group): 1,200 personnel

Total: ~4,300 personnel

---

**User:** Daily fuel use during offensive ops?

**Assistant:** Daily fuel consumption at OFFENSIVE tempo:
| Unit | Fuel (m³/day) |
|------|---------------|
| MEU-CE | 15 |
| BLT-1/5 | 45 |
| ACE-31 | 520 |
| LCE-15 | 30 |
| ARG-1 | 240 |
| **Total** | **850** |

ACE-31 uses 61% of total fuel due to aviation operations.

---

## The Data

`meu_logistics_data.csv` contains 54 tables:

| Category | Example Tables |
|----------|----------------|
| Units | unit_reference, unit_daily_demand |
| Supply | ammo_breakdown, fuel_consumption |
| Infrastructure | seaport_throughput, airfield_throughput |
| Equipment | vehicle_inventory, aircraft_inventory |
| Personnel | personnel_breakdown, personnel_consumption_rates |
| Operations | tempo_timeline_14_day, interdiction_probability |

---

## Implementation Checklist

- [ ] Import gradio, openai, dotenv
- [ ] Load environment variables
- [ ] Create OpenAI client
- [ ] Load CSV data as string
- [ ] Define system prompt with data embedded
- [ ] Create chat() function that:
  - [ ] Takes message and history
  - [ ] Builds messages array
  - [ ] Calls OpenAI API
  - [ ] Returns response text
- [ ] Create gr.ChatInterface with:
  - [ ] chat function
  - [ ] title
  - [ ] description
  - [ ] example questions
- [ ] Call .launch()

---

## Customization

**Change the model:**
```python
model="gpt-5.2"  # or "gpt-4o-mini" for lower cost
```

**Change the persona:**
Edit the SYSTEM_PROMPT to change how the assistant responds.

**Use different data:**
Replace `meu_logistics_data.csv` with any text/CSV file.

**Add authentication:**
```python
.launch(auth=("username", "password"))
```

**Share publicly:**
```python
.launch(share=True)  # Creates public URL
```

---

## Dependencies

```
gradio>=4.0.0
openai>=1.0.0
python-dotenv>=1.0.0
```

---

## Success Criteria

1. **Works**: User can chat and get answers about MEU data
2. **Simple**: Under 30 lines of code
3. **Fast**: Setup in under 5 minutes
4. **Accurate**: Responses include correct values from dataset

---

## Out of Scope

- ❌ RAG / embeddings
- ❌ Vector databases
- ❌ Custom frontend code
- ❌ User authentication
- ❌ Database storage
- ❌ Streaming responses

Keep it simple. This is for learning.
