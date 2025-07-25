import os
from dotenv import load_dotenv
from redisvl.extensions.router import SemanticRouter, Route
from redisvl.utils.vectorize import HFTextVectorizer

# Load environment variables
load_dotenv()

# === CONFIG ===
# Use REDIS_URL from env or fallback to default localhost
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# === ROUTES ===

technology = Route(
    name="technology",
    references=[
        "what are the latest advancements in AI?",
        "tell me about the newest gadgets",
        "what's trending in tech?",
        "news on quantum computing",
        "is 5G available everywhere?",
        "explain edge computing"
    ],
    metadata={"category": "tech"},
    distance_threshold=0.71
)

sports = Route(
    name="sports",
    references=[
        "who won the game last night?",
        "upcoming sports events",
        "latest news in the sports world",
        "results for NBA and NFL",
        "cricket match updates",
        "Olympics schedule",
        "jogo do curintia"
    ],
    metadata={"category": "sports"},
    distance_threshold=0.72
)

entertainment = Route(
    name="entertainment",
    references=[
        "top movies right now",
        "who won the Oscars?",
        "celebrity news",
        "upcoming TV shows and films",
        "trending series on Netflix",
        "what's new in the entertainment world?"
    ],
    metadata={"category": "entertainment"},
    distance_threshold=0.7
)

finance = Route(
    name="finance",
    references=[
        "latest stock market trends",
        "bitcoin price update",
        "how to invest in ETFs?",
        "interest rate changes",
        "best budgeting tips",
        "explain inflation"
    ],
    metadata={"category": "finance"},
    distance_threshold=0.73
)

health = Route(
    name="health",
    references=[
        "tips for mental health",
        "how to lose weight safely?",
        "symptoms of flu and covid",
        "healthy diets and routines",
        "benefits of meditation",
        "latest health research"
    ],
    metadata={"category": "health"},
    distance_threshold=0.74
)

travel = Route(
    name="travel",
    references=[
        "top destinations for 2025",
        "is Japan open for travel?",
        "budget travel tips",
        "visa requirements for US",
        "backpacking through Europe",
        "travel safety advice"
    ],
    metadata={"category": "travel"},
    distance_threshold=0.72
)

education = Route(
    name="education",
    references=[
        "best online learning platforms",
        "AI in classrooms",
        "how to learn coding",
        "top universities in Europe",
        "study tips for students",
        "education trends"
    ],
    metadata={"category": "education"},
    distance_threshold=0.73
)

food = Route(
    name="food",
    references=[
        "best recipes for dinner",
        "easy vegan meals",
        "restaurants near me",
        "what's trending in food?",
        "how to cook steak properly",
        "healthy snacks ideas"
    ],
    metadata={"category": "food"},
    distance_threshold=0.71
)

# === SEMANTIC ROUTER ===

router = SemanticRouter(
    name="topic-router",
    redis_url=REDIS_URL,
    vectorizer=HFTextVectorizer(),
    routes=[
        technology,
        sports,
        entertainment,
        finance,
        health,
        travel,
        education,
        food
    ],
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