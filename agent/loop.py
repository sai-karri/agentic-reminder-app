import os
import json
from datetime import datetime

from dotenv import load_dotenv

from agent.tools.definitions import ALL_TOOLS
from agent.tools.handlers import execute_tool

load_dotenv()

MAX_ITERATIONS = 5


def _build_system_prompt() -> str:
    now = datetime.now()
    return (
        "You are a personal reminder assistant. You help the user create, "
        "manage, and track reminders. "
        f"The current date and time is {now:%A, %B %d, %Y at %I:%M %p}. "
        "When the user asks to create a reminder with a time, always set a priority "
        "(default to medium if they don't specify). "
        "When you need a reminder's ID for completing, snoozing, or deleting, "
        "call list_reminders first to find it."
    )


# --- Gemini backend ---

def _init_gemini():
    from google import genai
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def _chat_gemini(client, user_message: str) -> str:
    from google.genai import types

    tools = types.Tool(function_declarations=ALL_TOOLS)
    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=_build_system_prompt(),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)],
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    for _ in range(MAX_ITERATIONS):
        part = response.candidates[0].content.parts[0]

        if part.function_call:
            name = part.function_call.name
            args = dict(part.function_call.args)
            tool_result = execute_tool(name, args)

            contents.append(response.candidates[0].content)
            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=name,
                            response={"result": tool_result},
                        )
                    ],
                )
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )
            continue

        if part.text:
            return part.text

        break

    return "Sorry, I couldn't process that. Please try again."


# --- Ollama backend ---

def _chat_ollama(model_name: str, user_message: str) -> str:
    import ollama

    ollama_tools = []
    for tool in ALL_TOOLS:
        ollama_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
        })

    messages = [
        {"role": "system", "content": _build_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    response = ollama.chat(
        model=model_name,
        messages=messages,
        tools=ollama_tools,
    )

    for _ in range(MAX_ITERATIONS):
        msg = response.message

        if msg.tool_calls:
            messages.append(msg)

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments
                tool_result = execute_tool(name, args)

                messages.append({
                    "role": "tool",
                    "content": json.dumps(tool_result),
                })

            response = ollama.chat(
                model=model_name,
                messages=messages,
                tools=ollama_tools,
            )
            continue

        if msg.content:
            return msg.content

        break

    return "Sorry, I couldn't process that. Please try again."


if __name__ == "__main__":
    print("Reminder Agent")
    print("-" * 40)
    print("Choose your LLM backend:")
    print("  1. Gemini (cloud, needs API key)")
    print("  2. Ollama (local, needs Ollama running)")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        backend = "gemini"
        client = _init_gemini()
        print(f"\nUsing Gemini 2.5 Flash")
    else:
        backend = "ollama"
        client = None
        model = input("Ollama model name (e.g. qwen3:4b): ").strip() or "qwen3:4b"
        print(f"\nUsing Ollama ({model})")

    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break

        if backend == "gemini":
            result = _chat_gemini(client, user_input)
        else:
            result = _chat_ollama(model, user_input)

        print(f"\nAgent: {result}\n")