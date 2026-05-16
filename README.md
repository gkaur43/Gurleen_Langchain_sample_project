# Recipe Generator - LangChain Single Agent Project

A beginner-friendly project that teaches you how to build a **single agent** using **LangChain + OpenAI**. The agent takes a list of available ingredients you have at home and generates a complete recipe along with beginner-friendly, step-by-step cooking instructions.

## What You'll Learn

- How LangChain works (LLMs, prompts, tools, agents)
- How to create tools using the `@tool` decorator
- How an agent decides which tools to call and in what order
- How `PromptTemplate` shapes LLM output
- How the agent's tool-calling loop works (think -> act -> observe -> repeat)

## How It Works

```text
User's ingredient list
       |
       v
  [Agent thinks: "I need to suggest a recipe first"]
       |
       v
  [Tool: suggest_recipe] --> suggests a suitable dish based on ingredients
       |
       v
  [Agent thinks: "Now I should generate the cooking steps"]
       |
       v
  [Tool: generate_cooking_steps] --> creates beginner-friendly steps with timings
       |
       v
  Final recipe guide returned to user
```

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Gurleen_Langchain_sample_project.git
cd Gurleen_Langchain_sample_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual OpenAI API key:

```text
OPENAI_API_KEY=sk-your-actual-key-here
```

## Run

```bash
python recipe_generator.py
```

You'll see an interactive prompt:

```text
Enter the ingredients you have at home: 
```

Type your ingredients (e.g., `potatoes, cauliflower, onions, tomatoes, rice`) and the agent will generate a recipe. You'll also see detailed logs showing the agent's reasoning and tool calls.

## Example

**Input:**
```text
potatoes, cauliflower, onions, tomatoes, rice
```

**Output:**
```text
Recipe Name: Aloo Gobi with Tomato-Onion Masala over Rice

Description:
A classic Indian comfort food featuring spiced potatoes and cauliflower in a flavorful tomato-onion gravy, perfectly served with steamed rice. Simple, hearty, and uses all your available ingredients!

Ingredients:
- 3 medium Potatoes (peeled and cubed)
- 1 medium Cauliflower head (cut into small florets)
- 2 medium Onions (finely chopped)
- 2 medium Tomatoes (chopped or pureed)
- 1 cup Rice
- 2 tbsp Cooking oil (pantry staple)
- 1 tsp Cumin seeds (pantry staple)
- 1 tsp Turmeric powder (pantry staple)
- 1 tsp Chili powder (pantry staple)
- Salt to taste (pantry staple)

Cooking Steps:
Step 1: Rinse 1 cup rice under cold water 2-3 times. Add to a pot with 2 cups water, pinch of salt. Bring to boil, then simmer covered for 12-15 minutes until fluffy. Fluff with fork and keep warm.
Step 2: Heat 2 tbsp oil in a large pan or wok over medium heat. Add 1 tsp cumin seeds and let them sizzle for 20 seconds.
Step 3: Add chopped onions and sauté for 4-5 minutes until golden brown.
Step 4: Add chopped tomatoes, 1 tsp turmeric, 1 tsp chili powder, and salt. Cook for 5-7 minutes until tomatoes break down into a thick masala paste.
Step 5: Add potato cubes first. Stir well to coat with masala. Cover and cook for 8 minutes on medium heat, stirring occasionally.
Step 6: Add cauliflower florets. Gently mix with the masala and potatoes. Add 1/4 cup water, cover, and cook for 10-12 minutes until vegetables are tender but not mushy.
Step 7: Taste and adjust salt/spice. Garnish with fresh cilantro if available. Serve hot with the steamed rice.

Prep Time: 15 minutes | Cook Time: 35 minutes | Serves: 3-4

Pro Tip: Squeeze fresh lemon juice on top before eating for extra zing! Perfect weeknight dinner using exactly what you have at home. 😋
```

## Project Structure

```text
.
├── recipe_generator.py  # Main agent code (fully commented)
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── .gitignore           # Keeps secrets and venv out of git
└── README.md            # This file
```

## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4.1-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
