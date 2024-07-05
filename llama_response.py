import json
import requests

def get_llama_response(query, top_tours, top_documents):
    # create the prompt
    prompt = """
    You are a bot that makes recommendations for holidays. You answer with facts, highlighting pros and cons.
    These are the recommended holidays: {top_documents}
    These are the tour names: {top_tours}
    The user input is: {query}
    Compile a recommendation to the user based on the recommended activities and the user input.
    """
    # setup llama3
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama3",
        "prompt": prompt.format(query=query, top_tours=top_tours, top_documents=top_documents)
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    # generate and return the response
    full_response = []
    try:
        count = 0
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                
                full_response.append(decoded_line['response'])
    finally:
        response.close()
    
    return full_response