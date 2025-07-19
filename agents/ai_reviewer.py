import os
import time
import json
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

# load GROQ API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# file paths
input_file = Path("agents/spun_chapter.txt")
output_file = Path("agents/reviewed_chapter.txt")
log_file = Path("scraping/reward_log.json")

def log_feedback(success, message):
    reward = 1 if success else -1
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "review_success": success,
        "message": message,
        reward: reward
    }
    logs = []
    if log_file.exists():
        logs = json.loads(log_file.read_text(encoding='utf-8'))
    logs.append(entry)
    log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

def review_chapter():
    if not input_file.exists():
        print("spun_chapter.txt does not exist. Please run the ai_writer.py first.")
        return
    
    spun_text = input_file.read_text(encoding='utf-8')

    print("Sending text to LLAMA for review...")

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system",
                "content": "You are an AI expert book editor. Give constructive feedback, point out flaws or awkward areas, and suggest improvements."},
                {"role": "user", "content": spun_text}
            ],
            max_tokens=2048,
            temperature=0.6
        )

        reviewed = response.choices[0].message.content
        output_file.write_text(reviewed, encoding='utf-8')
        print("Review completed successfully. Output written to reviewed_chapter.txt")
        log_feedback(True, "Review completed successfully.")
    except Exception as e:
        print("Error during review : ",e)
        log_feedback(False, str(e))
        
if __name__ == "__main__":
    review_chapter()
    print("Review process finished.")