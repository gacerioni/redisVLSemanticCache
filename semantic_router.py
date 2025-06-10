import os
from redisvl.extensions.router import SemanticRouter, Route
from redisvl.utils.vectorize import HFTextVectorizer

# === CONFIG ===
REDIS_URL = "redis://localhost:6379"

# Avoid tokenizer noise
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Define routes
technology = Route(
    name="technology",
    references=[
        "what are the latest advancements in AI?",
        "tell me about the newest gadgets",
        "what's trending in tech?"
    ],
    metadata={"category": "tech"},
    distance_threshold=0.71
)

sports = Route(
    name="sports",
    references=[
        "who won the game last night?",
        "tell me about the upcoming sports events",
        "what's the latest in the world of sports?",
        "sports",
        "basketball and football"
    ],
    metadata={"category": "sports"},
    distance_threshold=0.72
)

entertainment = Route(
    name="entertainment",
    references=[
        "what are the top movies right now?",
        "who won the best actor award?",
        "what's new in the entertainment industry?"
    ],
    metadata={"category": "entertainment"},
    distance_threshold=0.7
)

# Init semantic router
router = SemanticRouter(
    name="topic-router",
    redis_url=REDIS_URL,
    vectorizer=HFTextVectorizer(),
    routes=[technology, sports, entertainment],
    overwrite=True
)

def main():
    print("Semantic Router Demo — type 'exit' to quit")
    while True:
        question = input("Query: ").strip()
        if question.lower() == "exit":
            break

        match = router(question)
        if match.name:
            print(f"Matched route: {match.name} (distance={match.distance:.4f})")
        else:
            print("No route matched.")
        print()

if __name__ == "__main__":
    main()