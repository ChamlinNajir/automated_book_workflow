import os 
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")   

# Initialize Groq client
client = Groq(api_key=api_key)

# input/output file paths
input_file = Path("scraping/chapter_text.txt")
output_file = Path("agents/spun_chapter.txt")

def spin_chapter():
    if not input_file.exists():
        print("chapter_text.txt not found. Please ensure the scraping was complete.")
        return
    
    original_text = input_file.read_text(encoding='utf-8')

    print("Sending chapter to LLAMA-3 model...")

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative book editor. Rewrite this chapter to sound fresh and original while maintaining the original meaning."
                },
                {
                    "role": "user",
                    "content": original_text
                }
            ],
            max_tokens=2048,
            temperature=0.8
        )

        spun_text = response.choices[0].message.content
        output_file.write_text(spun_text, encoding='utf-8')
        print("Rewritten chapter saved to agents/spun_chapter.txt")

    except Exception as e:
        print("An error occurred while processing the chapter :", e)

if __name__ == "__main__":
    spin_chapter()