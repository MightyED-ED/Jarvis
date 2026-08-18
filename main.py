#print ('Hello, world')

#def green( a, b):
    #return a +b 

#result = green(1,2)
#print(result)

import ollama

# ---- TOOLS: each one is a normal function, tested on its own ----

def check_disk_space() -> float:
    """Check how much free disk space is available on the C: drive, in GB."""
    import shutil
    total, used, free = shutil.disk_usage("/")
    return round(free / (1024 * 1024 * 1024), 2)

# --- openes applications
def open_app(app_name: str) -> str:
    import subprocess
    try:
        subprocess.Popen(app_name)
        return f"Opened {app_name}"
    except FileNotFoundError:
        return f"Could not find an application called {app_name}"

# ---- TOOL REGISTRY: maps a tool's name -> the real function to run ----
available_tools = {
    "check_disk_space": check_disk_space,
    "open_app": open_app
}



# ---- TOOL SCHEMAS: what the model actually reads to decide when to use a tool ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_disk_space",
            "description": "Check how much free disk space is available on the C: drive, in GB.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application by its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open."
                    }
                },
                "required": ["app_name"]
            }
        }
    }
]

conversation = [
    {"role": "system", "content": "Your nickname is MightyED. Always refer to yourself as MightyED, and refer to the user as Eathon."}
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    conversation.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3.1:8b",
        messages=conversation,
        tools=tools
    )

    message = response['message']

    if message.get('tool_calls'):
        conversation.append(message)

        # Loop through EVERY tool the model wants to call, not just one
        for call in message['tool_calls']:
            tool_name = call['function']['name']
            tool_args = call['function']['arguments']
            function_to_run = available_tools[tool_name]   # look it up dynamically
            result = function_to_run(**tool_args)  # call it with the arguments the model provided  

            conversation.append({"role": "tool", "content": str(result)})

        final = ollama.chat(model="llama3.1:8b", messages=conversation)
        ai_reply = final['message']['content']
    else:
        ai_reply = message['content']

    print("MightyED:", ai_reply)
    conversation.append({"role": "assistant", "content": ai_reply})