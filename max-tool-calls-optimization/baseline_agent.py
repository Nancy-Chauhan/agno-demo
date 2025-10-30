from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

print("\n" * 2)
print("=" * 65)
print("⚠️  BASELINE AGENT - WITHOUT max_tool_calls_from_history")
print("=" * 65)
print()

# WITHOUT max_tool_calls_from_history
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    add_history_to_context=True,
    instructions="You are a research assistant. Be very brief - 1-2 sentences max.",
)

queries = [
    "What are the latest AI developments?",
    "How about quantum computing breakthroughs?",
    "Tell me about recent machine learning advances",
    "What's new in LLM research?",
    "Any breakthroughs in computer vision?",
    "What's happening with robotics AI?",
    "Latest in natural language processing?",
    "New developments in reinforcement learning?",
    "What's new in generative AI?",
    "Any advances in AI safety research?",
    "Tell me about neural architecture search",
    "What's happening with transformer models?",
    "Any news on AI ethics?",
    "Latest in edge AI computing?",
    "What's new in federated learning?",
    "Tell me about AI in healthcare",
    "What's happening with AI chips?",
    "Any advances in multimodal AI?",
    "Latest in AI for climate change?",
    "What's new in AI interpretability?",
    "What's new in prompt engineering?",
    "Latest in autonomous AI agents?",
    "AI for code generation updates?",
    "What's happening with AI regulation?",
    "Any breakthroughs in few-shot learning?",
    "Tell me about AI in drug discovery",
    "What's new in speech recognition?",
    "Latest in AI hardware acceleration?",
    "Any advances in continual learning?",
    "What's happening with AI alignment research?",
]

total_tool_calls = 0

for i, query in enumerate(queries, 1):
    print(f"🔍 Query {i}/{len(queries)}:")
    print("-" * 65)
    response = agent.run(query)
    print(response.content)
    
    # Count tool calls from this response
    if hasattr(response, 'messages'):
        tool_calls_this_query = sum(1 for msg in response.messages if hasattr(msg, 'role') and msg.role == 'tool')
        total_tool_calls += tool_calls_this_query
    
    if i < len(queries):
        print()

# Get metrics
print("\n" + "=" * 65)
print("📊 FINAL STATISTICS")
print("=" * 65)

# Try to get metrics
metrics = None
if hasattr(response, 'metrics') and response.metrics:
    metrics = response.metrics
elif hasattr(agent, 'metrics') and agent.metrics:
    metrics = agent.metrics

if metrics:
    input_tokens = getattr(metrics, 'input_tokens', 0)
    output_tokens = getattr(metrics, 'output_tokens', 0)
    total_tokens = getattr(metrics, 'total_tokens', 0)
    
    # Calculate cost (GPT-4o pricing)
    input_cost = input_tokens * 0.0025 / 1000
    output_cost = output_tokens * 0.010 / 1000
    total_cost = input_cost + output_cost
    
    # Calculate growth metrics
    if total_tool_calls > 0:
        context_growth_rate = 100.0  # All tool calls kept = 100% growth
        avg_tool_calls_per_query = total_tool_calls / len(queries)
    else:
        context_growth_rate = 0
        avg_tool_calls_per_query = 0
    
    print()
    print(f"  Queries Made:                   {len(queries)}")
    print(f"  Total Tool Calls Made:          {total_tool_calls}")
    print(f"  Total Tool Calls in Context:    {total_tool_calls}")
    print()
    print(f"  Input Tokens:         {input_tokens:>10,}")
    print(f"  Output Tokens:        {output_tokens:>10,}")
    print(f"  Total Tokens:         {total_tokens:>10,}  (0% savings - all kept!)")
    print()
    print(f"  Total Cost:           $    {total_cost:>7.4f}  (0% savings - baseline)")
    print()
    print("=" * 65)
    print("⚠️  WARNING - WITHOUT max_tool_calls_from_history:")
    print(f"  • ALL {total_tool_calls} tool calls kept in context!")
    print(f"  • 0 tool calls excluded = 0% optimization")
    print()
    print(f"  📈 Context Growth Problem:")
    print(f"     - Tool Call Retention:  {context_growth_rate:>5.1f}% (ALL kept!)")
    print(f"     - Avg per query:        {avg_tool_calls_per_query:>5.1f} tool calls")
    print(f"     - Growth rate:          Linear (unbound)")
    print()
    print("  ⚠️  Scaling Issues:")
    print("     - Context grows with EVERY query")
    print("     - WILL hit context limits at scale!")
    print("     - Token usage compounds exponentially")
    print()
    print(f"  💸 At 100 queries: ~{int(avg_tool_calls_per_query * 100)} tool calls in context!")
    print("=" * 65)
else:
    # Calculate growth metrics even without metrics
    if total_tool_calls > 0:
        context_growth_rate = 100.0
        avg_tool_calls_per_query = total_tool_calls / len(queries)
    else:
        context_growth_rate = 0
        avg_tool_calls_per_query = 0
    
    print()
    print(f"  Queries Made:                   {len(queries)}")
    print(f"  Total Tool Calls Made:          {total_tool_calls}")
    print(f"  Total Tool Calls in Context:    {total_tool_calls}")
    print()
    print("  📊 Could not retrieve token metrics")
    print("  💡 0% savings - all tool calls kept in context")
    print()
    print("=" * 65)
    print("⚠️  WARNING - WITHOUT max_tool_calls_from_history:")
    print(f"  • ALL {total_tool_calls} tool calls kept in context!")
    print(f"  • 0 tool calls excluded = 0% optimization")
    print()
    print(f"  📈 Context Growth Problem:")
    print(f"     - Tool Call Retention:  {context_growth_rate:>5.1f}% (ALL kept!)")
    print(f"     - Avg per query:        {avg_tool_calls_per_query:>5.1f} tool calls")
    print(f"     - Growth rate:          Linear (unbound)")
    print()
    print("  ⚠️  Scaling Issues:")
    print("     - Context grows with EVERY query")
    print("     - WILL hit context limits at scale!")
    print("     - Token usage compounds exponentially")
    print()
    print(f"  💸 At 100 queries: ~{int(avg_tool_calls_per_query * 100)} tool calls in context!")
    print("=" * 65)

print()
