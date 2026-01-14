# MEU Logistics Chat Agent

A chatbot that answers questions about Marine Expeditionary Unit logistics data. ~40 lines of Python.

## Quick Start

```bash
# Install
pip install gradio openai python-dotenv

# Setup (API key is pre-filled)
cp .env.example .env

# Run
python app.py
```

Opens automatically at http://localhost:7860

## How It Works

The entire 85KB logistics dataset goes into the system prompt. GPT handles it directly—no RAG, no embeddings, no complexity.

## Example Questions

- "What units make up the MEU?"
- "What's the daily fuel consumption during offensive operations?"
- "Compare Guam and Darwin port capacities"
- "What aircraft does the ACE have?"

## Files

| File | Description |
|------|-------------|
| `app.py` | The entire application |
| `meu_logistics_data.csv` | 54 tables of MEU logistics data |
| `PRD.md` | Full spec (for understanding/extending) |

## Customization

Change the model in `app.py`:
```python
model="gpt-4o"  # or gpt-4o-mini, gpt-5.2, etc.
```

Share publicly:
```python
.launch(share=True)
```
