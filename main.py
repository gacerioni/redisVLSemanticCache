#############################
# === CONFIGURATION PANEL ===
DISTANCE_THRESHOLD = 0.3
VECTOR_MODEL = "redis/langcache-embed-v1"
CACHE_NAME = "llmcache"
user_id = "user_gabs_123"
#############################

from dotenv import load_dotenv
import os
import time
import numpy as np

from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query.filter import Tag
from openai import OpenAI

# Load environment variables
load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "False"

# Get API key from env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")

# Get Redis URL from env (fallback to default localhost if not provided)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

client = OpenAI(api_key=api_key)

def ask_openai(question: str) -> str:
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=question,
        max_tokens=200
    )
    return response.choices[0].text.strip()

llmcache = SemanticCache(
    name=CACHE_NAME,
    redis_url=REDIS_URL,
    distance_threshold=DISTANCE_THRESHOLD,
    vectorizer=HFTextVectorizer(VECTOR_MODEL),
    filterable_fields=[{"name": "user_id", "type": "tag"}],
    overwrite=True
)

def get_answer_with_cache(question: str, user_id: str):
    filter_by_user = Tag("user_id") == user_id
    start = time.time()
    cached = llmcache.check(prompt=question, filter_expression=filter_by_user)
    if cached:
        cache_status = "HIT"
        response = cached[0]["response"]
    else:
        cache_status = "MISS"
        response = ask_openai(question)
        llmcache.store(prompt=question, response=response, filters={"user_id": user_id})
    duration = time.time() - start
    return response, duration, cache_status

def chatbot_loop():
    print("Welcome to the semantic cache chatbot. Type 'exit' to quit.")
    while True:
        print("#####################################################")
        question = input("Enter your question: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break
        answer, duration, cache_status = get_answer_with_cache(question, user_id)
        print(f"Cache {cache_status}")
        print(f"Answer: {answer}")
        print(f"Response time: {duration:.4f}s\n")

def main():
    llmcache.clear()
    chatbot_loop()

main()