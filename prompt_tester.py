import csv
import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPTS

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

def test_prompt(task, prompt_name, prompt_template):
    """Send a task through a prompt template and return the response."""
    formatted_prompt = prompt_template.format(task=task)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": formatted_prompt}]
    )
    
    return response.choices[0].message.content

def run_tests():
    """Read test cases from CSV, run through all prompts, save results."""
    results = []
    
    # Read test cases
    with open("inputs/test_cases.csv", "r") as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)
    
    print(f"Running {len(test_cases)} test cases across {len(PROMPTS)} prompts...\n")
    
    for test in test_cases:
        task = test["task"]
        print(f"Testing: {task[:50]}...")
        
        for prompt_name, prompt_template in PROMPTS.items():
            print(f"  → {prompt_name} prompt")
            
            output = test_prompt(task, prompt_name, prompt_template)
            
            results.append({
                "task": task,
                "prompt_style": prompt_name,
                "output": output
            })
            
            time.sleep(1)  # Respect rate limits
    
    # Save results to CSV
    with open("outputs/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["task", "prompt_style", "output"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✅ Done! Results saved to outputs/results.csv")

if __name__ == "__main__":
    run_tests()
