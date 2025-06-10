# RedisVL Semantic Cache Chatbot

This is a minimal chatbot demo that uses **RedisVL** as a semantic cache to reduce LLM calls, improve performance, and demonstrate cache hits vs misses in real time.

## 🔧 Features

- Semantic caching using vector similarity
- Supports per-user cache isolation via tags
- Uses OpenAI API (GPT-3.5) for fallback
- Shows latency and cache usage for each response

## 🧠 How It Works

1. You ask a question.
2. The app checks Redis for a semantically similar cached response.
3. If found (`Cache HIT`), it returns instantly.
4. If not (`Cache MISS`), it queries OpenAI, returns the answer, and stores it in Redis for future use.

## 🚀 Quickstart

1. Clone this repo and install dependencies:

```bash
pip install -r requirements.txt