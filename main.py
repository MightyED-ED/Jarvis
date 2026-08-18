#print ('Hello, world')

#def green( a, b):
    #return a +b 

#result = green(1,2)
#print(result)

import ollama

#fucntion to check disk space
def check_disk_space() -> float:
        import shutil
        total, used, free = shutil.disk_usage("/")
        return free / (1024 * 1024 * 1024)  # Return free space in GB

disk_space = check_disk_space()


# Conversation history starts with the system message setting identity
conversation = [
    {"role": "system", "content": "Your nickname is MightyED. Always refer to yourself as MightyED, and refer to the user as Eathon."},
    {"role":"system", "content": f"how much disk space is available{disk_space}"}
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    conversation.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3.1:8b",
        messages=conversation,
        tools=[check_disk_space])

    message = response["tool_calls"]
    if message.get('tool_calls'):
        result = check_disk_space()
        conversation.append(message)
        conversation.append({"role":"tool","content":str(result)})

        final = ollama.chat(model="llama3.1:8b", messages=conversation)
        ai_reply = final['message']['content']
    else:
        ai_reply = message['content']

    
    print("MightyED:", ai_reply)
    conversation.append({"role": "assistant", "content": ai_reply})