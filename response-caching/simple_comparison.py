"""
Response Caching Demo: Side-by-Side Comparison

This demo shows a direct comparison between running the same query 5 times
with and without caching enabled.

Perfect for quickly demonstrating the impact of response caching.
"""

import time
from agno.agent import Agent
from agno.models.openai import OpenAIChat

print("=" * 60)
print("DEMO: Response Caching Impact")
print("=" * 60)

# Test WITHOUT caching
print("\n🔴 WITHOUT CACHING:")
agent_no_cache = Agent(
    model=OpenAIChat(id="gpt-4o-mini", cache_response=False)
)

start = time.time()
total_tokens_no_cache = 0
for i in range(5):
    print(f"  Run {i+1}...", end=" ", flush=True)
    response = agent_no_cache.run("What is the capital of France?")
    total_tokens_no_cache += response.metrics.total_tokens
    print(f"{time.time() - start:.2f}s")
    
total_no_cache = time.time() - start
print(f"\n⏱️  Total time: {total_no_cache:.2f}s")
print(f"💰 Total cost: ~${total_tokens_no_cache * 0.000001 * 5:.4f}")

# Test WITH caching
print("\n🟢 WITH CACHING:")
agent_with_cache = Agent(
    model=OpenAIChat(id="gpt-4o-mini", cache_response=True)
)

start = time.time()
total_tokens_with_cache = 0
for i in range(5):
    print(f"  Run {i+1}...", end=" ", flush=True)
    response = agent_with_cache.run("What is the capital of France?")
    if i == 0:
        total_tokens_with_cache = response.metrics.total_tokens
    elapsed = time.time() - start
    print(f"{elapsed:.2f}s {'✨ CACHED!' if i > 0 else '📡 API call'}")
    
total_with_cache = time.time() - start

print(f"\n⏱️  Total time: {total_with_cache:.2f}s")
print(f"💰 Total cost: ~${total_tokens_with_cache * 0.000001:.4f}")

# Impact Summary
print("\n" + "=" * 60)
print("📊 IMPACT SUMMARY:")
print("=" * 60)
speedup = total_no_cache / total_with_cache
savings = ((1 - (total_tokens_with_cache / (total_tokens_no_cache * 5))) * 100)
print(f"⚡ Speed improvement: {speedup:.1f}x faster")
print(f"💵 Cost savings: {savings:.0f}% reduction")
print(f"⏰ Time saved: {total_no_cache - total_with_cache:.2f} seconds")
