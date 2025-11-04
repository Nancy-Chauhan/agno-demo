"""
Response Caching Demo: Full Development Day Simulation

This demo simulates a realistic 8-hour development day building a customer support agent.
It demonstrates how response caching dramatically reduces API costs and speeds up iteration.

Key Metrics Shown:
- Total cost savings
- API calls avoided
- Cache hit rate
- Time saved
"""

import time
from agno.agent import Agent
from agno.models.openai import OpenAIChat

print("=" * 80)
print("📅 SIMULATION: Full Development Day (8 hours)")
print("Scenario: Building a customer support agent")
print("=" * 80)

# Realistic development scenarios throughout the day
scenarios = {
    "Morning (Testing password reset flow)": ("How do I reset my password?", 15),
    "Mid-morning (Testing order status)": ("Where is my order?", 12),
    "Lunch (Testing refund policy)": ("What's your refund policy?", 8),
    "Afternoon (Back to password reset)": ("How do I reset my password?", 10),
    "Late afternoon (Testing all queries)": ("How do I reset my password?", 5),
}

total_iterations = sum(count for _, count in scenarios.values())

print(f"\nTotal test iterations planned: {total_iterations}")
print("Testing with gpt-4o ($0.005 per 1k tokens)\n")

# WITH CACHING (Smart Development)
print("🟢 WITH CACHING (Smart Development):")
print("-" * 80)

agent = Agent(model=OpenAIChat(id="gpt-4o", cache_response=True))

start_day = time.time()
total_cost = 0
api_calls = 0
cache_hits = 0
query_cache = {}

for scenario, (query, count) in scenarios.items():
    print(f"\n{scenario}")
    for i in range(count):
        response = agent.run(query)
        
        if query not in query_cache:
            query_cache[query] = True
            api_calls += 1
            cost = response.metrics.total_tokens * 0.000005
            total_cost += cost
            print(f"  Iteration {i+1}: ${cost:.4f} (API)")
        else:
            cache_hits += 1
            if i == 0:
                print(f"  Iteration {i+1}: $0.0000 (CACHE ✨) - continuing cached...")

total_time = time.time() - start_day

print("\n" + "=" * 80)
print("📊 END OF DAY SUMMARY:")
print("=" * 80)
print(f"⏱️  Total development time: {total_time:.1f}s")
print(f"💰 Total cost: ${total_cost:.4f}")
print(f"📞 API calls: {api_calls}")
print(f"✨ Cache hits: {cache_hits}")
print(f"📈 Cache hit rate: {(cache_hits/total_iterations*100):.0f}%")

# WITHOUT CACHING comparison
cost_no_cache = total_iterations * 0.002  # Estimated cost per call
time_no_cache = total_iterations * 2  # Estimated 2s per call

print("\n" + "-" * 80)
print("🔴 IF YOU DIDN'T USE CACHING:")
print("-" * 80)
print(f"⏱️  Would have taken: ~{time_no_cache:.0f}s ({time_no_cache/60:.1f} minutes)")
print(f"💰 Would have cost: ~${cost_no_cache:.4f}")
print(f"📞 Would have made: {total_iterations} API calls")

print("\n" + "=" * 80)
print("💡 SAVINGS:")
print("=" * 80)
print(f"⚡ Time saved: {time_no_cache - total_time:.1f}s")
print(f"💵 Money saved: ${cost_no_cache - total_cost:.4f}")
print(f"📞 API calls avoided: {total_iterations - api_calls}")
print(f"\n🎯 You saved {((cost_no_cache - total_cost)/cost_no_cache*100):.0f}% of your API costs today!")
