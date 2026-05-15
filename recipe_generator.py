"""
===========================================================================
 RECIPE GENERATOR -- A Beginner's LangChain Single-Agent Project
===========================================================================

 WHAT THIS PROJECT TEACHES YOU:
   1. How LangChain works (chains, prompts, LLMs, tools, agents)
   2. How to build a SINGLE AGENT that uses tools
   3. How to connect LangChain to OpenAI
   4. How prompt templates shape LLM output
   5. How an agent "thinks" using a tool-calling loop

 HOW LANGCHAIN WORKS (the big picture):
   LangChain is a framework that makes it easy to build LLM-powered apps.

     [User Input] --> [Prompt Template] --> [LLM (GPT)] --> [Output]

   - Prompt Template : A reusable template with placeholders (like a form)
   - LLM            : The AI model that generates text (OpenAI GPT)
   - Output         : The generated response

 WHAT IS AN AGENT?
   An agent is an LLM that can USE TOOLS and DECIDE what to do next.
   Unlike a simple chain (input -> LLM -> output), an agent can:
     1. Think about what it needs to do
     2. Pick a tool to use
     3. Use the tool and see the result
     4. Decide if it needs more steps or if it's done

   This is the tool-calling loop:
     THINK -> ACT -> OBSERVE -> THINK -> ... -> FINAL ANSWER

 HOW THIS PROJECT FLOWS:
   1. User provides a list of ingredients (e.g., "potatoes, rice, onions, tomatoes")
   2. Agent calls suggest_recipe tool       -> creates a recipe based on ingredients
   3. Agent calls generate_cooking_steps tool -> creates beginner-friendly steps with timings
   4. Agent returns the final complete recipe guide to the user

 KEY LANGCHAIN COMPONENTS USED:
   - ChatOpenAI      : LLM wrapper that sends prompts to OpenAI's GPT API
   - PromptTemplate  : Template with {placeholders} filled before sending to LLM
   - @tool decorator : Turns a Python function into a tool the agent can call
   - create_agent    : Wires LLM + tools + system prompt into a runnable agent

 SETUP:
   1. pip install -r requirements.txt
   2. Copy .env.example to .env and add your OpenAI API key
   3. python recipe_generator.py

 See langchain_tutorial.md for a full beginner's guide to LangChain.
 See architecture_diagram.drawio for a visual diagram of this project.
===========================================================================
"""

import logging
import sys
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("RecipeGenerator")

logger.info("Starting Recipe Generator Agent...")

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set! Copy .env.example to .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    verbose=True,
)

logger.info("LLM initialized: model=gpt-4.1-mini, temperature=0.7")
logger.info("Defining agent tools...")


@tool
def suggest_recipe(ingredients: str) -> str:
    """
    Suggests a suitable dish that can be made using the available ingredients.
    Use this tool FIRST when the user provides their list of ingredients.
    Input should be a comma-separated list of available ingredients.
    Returns a recipe name, description, and full ingredient list with quantities.
    """
    logger.info(f"[Tool: suggest_recipe] Received ingredients: '{ingredients}'")

    recipe_prompt = PromptTemplate(
        input_variables=["ingredients"],
        template="""You are a friendly home chef.
Given the following ingredients, suggest a suitable dish to make.

Ingredients: {ingredients}

Write the suggestion with:
- A clear Recipe Name
- A short, appetizing description
- A full ingredient list with estimated quantities (you may allow 1-2 common pantry staples)

Return ONLY the recipe details, nothing else.""",
    )

    formatted_prompt = recipe_prompt.format(ingredients=ingredients)
    logger.info("[Tool: suggest_recipe] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: suggest_recipe] Recipe suggested successfully!")
    return response.content


@tool
def generate_cooking_steps(recipe_details: str) -> str:
    """
    Takes recipe details and converts them into numbered, beginner-friendly cooking steps with timings.
    Use this tool AFTER suggest_recipe to make a clear step-by-step cooking guide.
    Input should be the full recipe details text.
    Returns a clear step-by-step cooking guide.
    """
    logger.info("[Tool: generate_cooking_steps] Generating cooking steps for the recipe...")

    steps_prompt = PromptTemplate(
        input_variables=["recipe_details"],
        template="""You are a friendly home chef helping a beginner cook.

Take these recipe details and create a step-by-step cooking guide.

Rules:
- Make the steps numbered and chronological
- Ensure the language is beginner-friendly and encouraging
- Include estimated timings for each major step (e.g., "Simmer for 10 minutes")
- Keep it practical and easy to follow
- Keep the same core recipe intact

Recipe details:
{recipe_details}

Return ONLY the cooking steps, nothing else.""",
    )

    formatted_prompt = steps_prompt.format(recipe_details=recipe_details)
    logger.info("[Tool: generate_cooking_steps] Sending to LLM for step generation...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: generate_cooking_steps] Cooking steps generated successfully!")
    return response.content


tools = [suggest_recipe, generate_cooking_steps]
logger.info(f"Tools registered: {[t.name for t in tools]}")
logger.info("Creating the agent...")

SYSTEM_PROMPT = """You are a friendly home chef who helps users cook meals with what they already have.

When the user gives you a list of ingredients, follow these steps:
1. First, use the suggest_recipe tool to create a recipe suggestion.
2. Then, use the generate_cooking_steps tool to produce clear cooking instructions with timings.
3. Return the final recipe and steps to the user.

Always use both tools in order: suggest recipe first, then generate cooking steps."""

agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    debug=True,
)

logger.info("Agent created and ready to run!")


def run_recipe_generator(ingredients: str) -> str:
    """
    Main function to run the recipe generator agent.

    Args:
        ingredients: A comma-separated list of ingredients you have.
                     Example: "chicken, broccoli, soy sauce, rice"

    Returns:
        A complete recipe with step-by-step cooking instructions.
    """
    logger.info("=" * 60)
    logger.info(f"USER'S INGREDIENTS: {ingredients}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking... watch the tool-calling loop below!")
    logger.info("-" * 60)

    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=ingredients)]}
    )

    final_recipe = result["messages"][-1].content

    logger.info("-" * 60)
    logger.info("FINAL RECIPE GUIDE GENERATED")
    logger.info("-" * 60)

    return final_recipe


if __name__ == "__main__":
    user_ingredients = input("Enter the ingredients you have at home: ")
    output = run_recipe_generator(user_ingredients)
    print("\n" + "=" * 60)
    print("RECIPE GENERATOR OUTPUT")
    print("=" * 60)
    print(output)
