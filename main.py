#print ('Hello, world')

#def green( a, b):
    #return a +b 

#result = green(1,2)
#print(result)

import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{ "role":"user","content":"Hello, How are you?"}]
        
    
)

print(response['message']['content'])