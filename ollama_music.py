import requests
import argparse
import json

# OLLAMA_HOST = 'http://localhost:11434'  # Adjust if your Ollama server is running elsewhere
OLLAMA_HOST = 'http://localhost:3000'  # Adjust if your Ollama server is running elsewhere
MODEL = 'gemma3:4b'

# Define the music lover persona
MUSIC_LOVER_PERSONA = """You are an enthusiastic and knowledgeable music lover with a deep passion 
for all genres of music. You have:
- Extensive knowledge of music history, theory, and appreciation
- Personal experience attending countless concerts and musical performances
- A collection of thousands of albums across various genres
- Strong opinions about music while remaining respectful of others' tastes
- A warm, engaging personality that loves sharing musical discoveries
- The ability to explain complex musical concepts in an accessible way

Please maintain this personality in all your responses, sharing your enthusiasm 
and personal perspective while being informative and engaging."""

def query_ollama(query):
    url = f"{OLLAMA_HOST}/api/chat"
    headers = {'Content-Type': 'application/json'}
    
    # Include the persona as the system message and the user query
    messages = [
        {"role": "system", "content": MUSIC_LOVER_PERSONA},
        {"role": "user", "content": query}
    ]
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True  # Enable streaming for line-by-line processing
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)
    response.raise_for_status()
    
    # Process the streaming response
    full_response = ""
    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            if 'message' in json_response:
                content = json_response['message'].get('content', '')
                full_response += content
    
    return full_response

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Query the music-loving AI about any music topic.')
    parser.add_argument('query', type=str, help='Your music-related question or topic')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Get response from Ollama
        response = query_ollama(args.query)
        
        if response:
            print("\n🎵 Music Lover's Response:\n")
            print(response)
            print()  # Add a blank line at the end
        else:
            print("\nNo response received from the assistant.\n")
            
    except Exception as e:
        print(f"\nError: {str(e)}\n")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())


