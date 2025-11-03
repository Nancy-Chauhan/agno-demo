"""
Benchmark for Agno's max_tool_calls_from_history feature.

This script demonstrates token and cost savings by comparing:
- Baseline: Unlimited tool call history (context grows with each query)
- Optimized: Limited to 3 most recent tool calls (constant context size)

Results with 50 queries:
- 84.8% context reduction
- 56.1% token savings
- 55.6% cost savings

Official docs: https://docs.agno.com/examples/concepts/agent/context_management/filter_tool_calls_from_history
"""

import random
import time
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
import json
from datetime import datetime


def get_info_about_topic(topic: str) -> str:
    """Get information about a topic. This function ALWAYS gets called."""
    responses = [
        f"Latest research shows significant advances in {topic}.",
        f"Industry experts are excited about developments in {topic}.",
        f"Recent breakthroughs in {topic} are promising for the future.",
        f"Companies are investing heavily in {topic} technology.",
        f"Academic papers on {topic} have increased 50% this year.",
    ]
    return random.choice(responses)


# 50 diverse topics to query
BENCHMARK_QUERIES = [
    "AI developments", "quantum computing", "machine learning",
    "LLM research", "computer vision", "robotics AI",
    "natural language processing", "reinforcement learning", "generative AI",
    "AI safety", "neural architecture", "transformer models",
    "AI ethics", "edge AI", "federated learning",
    "AI healthcare", "AI chips", "multimodal AI",
    "OpenAI news", "Google AI", "Microsoft AI",
    "Meta AI", "Anthropic", "Tesla AI",
    "Apple ML", "Amazon AI", "NVIDIA AI",
    "Intel AI", "protein folding", "drug discovery AI",
    "climate AI", "renewable energy AI", "autonomous vehicles",
    "AI finance", "language generation", "medical imaging AI",
    "AI cybersecurity", "edge computing", "AI coding assistants",
    "AI image generation", "voice synthesis", "AI video generation",
    "AI music", "AI writing", "AI chatbots",
    "legal tech AI", "education AI", "agriculture AI",
    "manufacturing AI", "supply chain AI",
]


def run_baseline_agent(topics, verbose=False):
    """Baseline WITHOUT max_tool_calls_from_history"""
    print("\n" + "=" * 90)
    print("⚠️  BASELINE - WITHOUT max_tool_calls_from_history")
    print("=" * 90 + "\n")
    
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[get_info_about_topic],
        db=SqliteDb(db_file="tmp/baseline_guaranteed.db"),
        add_history_to_context=True,
        num_history_runs=None,  # ← UNLIMITED history for baseline!
        markdown=True,
        instructions="You are a research assistant. ALWAYS use get_info_about_topic to answer. Be brief.",
    )
    
    print(f"{'Run':<5} | {'Topic':<30} | {'History':<8} | {'Current':<8} | {'In Context':<11} | {'In DB':<8}")
    print("-" * 90)
    
    start_time = time.time()
    total_history_in_context = 0
    total_current_in_context = 0
    
    for i, topic in enumerate(topics, 1):
        run_response = agent.run(f"Tell me about {topic}", stream=False)
        
        # Official tracking method
        history_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and getattr(msg, "from_history", False)
        )
        
        current_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and not getattr(msg, "from_history", False)
        )
        
        total_in_context = history_tool_calls + current_tool_calls
        
        saved_messages = agent.get_messages_for_session()
        saved_tool_calls = sum(
            len(msg.tool_calls)
            for msg in saved_messages
            if msg.role == "assistant" and msg.tool_calls
        ) if saved_messages else 0
        
        total_history_in_context += history_tool_calls
        total_current_in_context += current_tool_calls
        
        if verbose or i <= 5 or i > len(topics) - 3:  # Show first 5 and last 3
            topic_short = topic[:30] if len(topic) > 30 else topic
            print(f"{i:<5} | {topic_short:<30} | {history_tool_calls:<8} | {current_tool_calls:<8} | {total_in_context:<11} | {saved_tool_calls:<8}")
        elif i == 6:
            print("  ... (showing first 5 and last 3 queries)")
    
    elapsed_time = time.time() - start_time
    metrics = run_response.metrics if hasattr(run_response, 'metrics') else None
    
    total_context_used = total_history_in_context + total_current_in_context
    avg_context = total_context_used / len(topics)
    
    print("\n" + "-" * 90)
    print(f"BASELINE SUMMARY:")
    print(f"  Total tool calls in DB:        {saved_tool_calls}")
    print(f"  Total context used (sum):      {total_context_used}")
    print(f"  Avg context per query:         {avg_context:.1f}")
    print(f"  Expected avg (no limit):       ~{(len(topics) + 1) / 2:.1f}")
    
    return {
        'agent_type': 'baseline',
        'queries_count': len(topics),
        'total_in_db': saved_tool_calls,
        'total_context_used': total_context_used,
        'avg_context_per_query': avg_context,
        'elapsed_time': elapsed_time,
        'metrics': metrics
    }


def run_optimized_agent(topics, max_history_limit=3, verbose=False):
    """Optimized WITH max_tool_calls_from_history"""
    print("\n" + "=" * 90)
    print(f"✅ OPTIMIZED - WITH max_tool_calls_from_history={max_history_limit}")
    print("=" * 90 + "\n")
    
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[get_info_about_topic],
        db=SqliteDb(db_file="tmp/optimized_guaranteed.db"),
        max_tool_calls_from_history=max_history_limit,
        add_history_to_context=True,
        num_history_runs=None,  # ← Unlimited RUNS, but limited tool calls!
        markdown=True,
        instructions="You are a research assistant. ALWAYS use get_info_about_topic to answer. Be brief.",
    )
    
    print(f"{'Run':<5} | {'Topic':<30} | {'History':<8} | {'Current':<8} | {'In Context':<11} | {'In DB':<8}")
    print("-" * 90)
    
    start_time = time.time()
    total_history_in_context = 0
    total_current_in_context = 0
    
    for i, topic in enumerate(topics, 1):
        run_response = agent.run(f"Tell me about {topic}", stream=False)
        
        # Official tracking method
        history_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and getattr(msg, "from_history", False)
        )
        
        current_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and not getattr(msg, "from_history", False)
        )
        
        total_in_context = history_tool_calls + current_tool_calls
        
        saved_messages = agent.get_messages_for_session()
        saved_tool_calls = sum(
            len(msg.tool_calls)
            for msg in saved_messages
            if msg.role == "assistant" and msg.tool_calls
        ) if saved_messages else 0
        
        total_history_in_context += history_tool_calls
        total_current_in_context += current_tool_calls
        
        if verbose or i <= 5 or i > len(topics) - 3:  # Show first 5 and last 3
            topic_short = topic[:30] if len(topic) > 30 else topic
            print(f"{i:<5} | {topic_short:<30} | {history_tool_calls:<8} | {current_tool_calls:<8} | {total_in_context:<11} | {saved_tool_calls:<8}")
        elif i == 6:
            print("  ... (showing first 5 and last 3 queries)")
    
    elapsed_time = time.time() - start_time
    metrics = run_response.metrics if hasattr(run_response, 'metrics') else None
    
    total_context_used = total_history_in_context + total_current_in_context
    avg_context = total_context_used / len(topics)
    
    print("\n" + "-" * 90)
    print(f"OPTIMIZED SUMMARY (limit={max_history_limit}):")
    print(f"  Total tool calls in DB:        {saved_tool_calls}")
    print(f"  Total context used (sum):      {total_context_used}")
    print(f"  Avg context per query:         {avg_context:.1f}")
    print(f"  Expected avg (with limit):     ~{max_history_limit + 1:.1f}")
    
    return {
        'agent_type': 'optimized',
        'queries_count': len(topics),
        'max_history_limit': max_history_limit,
        'total_in_db': saved_tool_calls,
        'total_context_used': total_context_used,
        'avg_context_per_query': avg_context,
        'elapsed_time': elapsed_time,
        'metrics': metrics
    }


def calculate_metrics(baseline_results, optimized_results):
    """Calculate comparison metrics"""
    
    def extract_token_metrics(metrics):
        if not metrics:
            return None
        return {
            'input_tokens': getattr(metrics, 'input_tokens', 0),
            'output_tokens': getattr(metrics, 'output_tokens', 0),
            'total_tokens': getattr(metrics, 'total_tokens', 0),
        }
    
    baseline_metrics = extract_token_metrics(baseline_results['metrics'])
    optimized_metrics = extract_token_metrics(optimized_results['metrics'])
    
    # Context reduction
    baseline_avg = baseline_results['avg_context_per_query']
    optimized_avg = optimized_results['avg_context_per_query']
    context_reduction_pct = ((baseline_avg - optimized_avg) / baseline_avg * 100) if baseline_avg > 0 else 0
    
    # Token and cost savings
    token_savings_pct = 0
    cost_savings_pct = 0
    baseline_cost = 0
    optimized_cost = 0
    
    if baseline_metrics and optimized_metrics and baseline_metrics['total_tokens'] > 0:
        token_diff = baseline_metrics['total_tokens'] - optimized_metrics['total_tokens']
        token_savings_pct = (token_diff / baseline_metrics['total_tokens']) * 100
        
        # GPT-4o-mini pricing
        baseline_cost = (baseline_metrics['input_tokens'] * 0.00015 + 
                        baseline_metrics['output_tokens'] * 0.0006)
        optimized_cost = (optimized_metrics['input_tokens'] * 0.00015 + 
                         optimized_metrics['output_tokens'] * 0.0006)
        
        if baseline_cost > 0:
            cost_savings_pct = ((baseline_cost - optimized_cost) / baseline_cost) * 100
    
    return {
        'baseline': {
            'queries_count': baseline_results['queries_count'],
            'total_in_db': baseline_results['total_in_db'],
            'avg_context_per_query': baseline_results['avg_context_per_query'],
            'metrics': baseline_metrics,
            'cost': baseline_cost,
            'elapsed_time': baseline_results['elapsed_time']
        },
        'optimized': {
            'queries_count': optimized_results['queries_count'],
            'max_history_limit': optimized_results['max_history_limit'],
            'total_in_db': optimized_results['total_in_db'],
            'avg_context_per_query': optimized_results['avg_context_per_query'],
            'metrics': optimized_metrics,
            'cost': optimized_cost,
            'elapsed_time': optimized_results['elapsed_time']
        },
        'savings': {
            'context_reduction_pct': context_reduction_pct,
            'token_savings_pct': token_savings_pct,
            'cost_savings_pct': cost_savings_pct
        }
    }


def print_comparison_report(comparison):
    """Print detailed comparison"""
    baseline = comparison['baseline']
    optimized = comparison['optimized']
    savings = comparison['savings']
    
    print("\n" + "=" * 90)
    print("📊 BENCHMARK COMPARISON RESULTS")
    print("=" * 90 + "\n")
    
    print("🔧 CONTEXT SIZE:")
    print("-" * 90)
    print(f"  Total tool calls in DB:        {baseline['total_in_db']}")
    print()
    print(f"  Baseline (no limit):")
    print(f"    • Avg context per query:     {baseline['avg_context_per_query']:.1f} tool calls")
    print()
    print(f"  Optimized (limit={optimized['max_history_limit']}):")
    print(f"    • Avg context per query:     {optimized['avg_context_per_query']:.1f} tool calls")
    print()
    print(f"  ✅ Context Reduction:          {savings['context_reduction_pct']:.1f}%")
    print()
    
    if baseline['metrics'] and optimized['metrics']:
        print("💰 TOKEN USAGE:")
        print("-" * 90)
        print(f"  Baseline:           {baseline['metrics']['total_tokens']:>10,} tokens")
        print(f"  Optimized:          {optimized['metrics']['total_tokens']:>10,} tokens")
        print(f"  ✅ Token Savings:   {savings['token_savings_pct']:>9.1f}%")
        print()
        
        print("💵 COST (GPT-4o-mini):")
        print("-" * 90)
        print(f"  Baseline:           ${baseline['cost']:>10.4f}")
        print(f"  Optimized:          ${optimized['cost']:>10.4f}")
        print(f"  ✅ Cost Savings:    {savings['cost_savings_pct']:>9.1f}%")
        print()
    
    print("=" * 90)


def generate_linkedin_post(comparison):
    """Generate LinkedIn post"""
    b = comparison['baseline']
    o = comparison['optimized']
    s = comparison['savings']
    
    return f"""
🚀 Massive Token & Cost Savings in AI Agent Development

I just benchmarked Agno's `max_tool_calls_from_history` feature with guaranteed tool calls, and the results are incredible:

📊 Results from {b['total_in_db']} tool calls across {b['queries_count']} queries:

WITHOUT optimization:
• Avg {b['avg_context_per_query']:.1f} tool calls in context per query
• Context grows linearly (1, 2, 3, 4... up to {b['total_in_db']})
• Will hit limits at scale ⚠️

WITH max_tool_calls_from_history={o['max_history_limit']}:
• Avg {o['avg_context_per_query']:.1f} tool calls in context per query
• Context stays bounded (1, 2, 3, then constant at {o['max_history_limit']+1})
• {s['context_reduction_pct']:.1f}% reduction in context size 🎯
• {s['token_savings_pct']:.1f}% token savings 💰
• {s['cost_savings_pct']:.1f}% cost savings 💸

Key insight: Complete history preserved in DB - you're just optimizing what the LLM sees in context!

Perfect for:
✅ Multi-turn agentic workflows
✅ Long-running conversations
✅ Production cost optimization

Try it: https://docs.agno.com/examples/concepts/agent/context_management/filter_tool_calls_from_history

#AI #LLM #AIAgents #CostOptimization #Agno
"""


def main():
    """Run guaranteed tool call benchmark"""
    print("\n🎯 GUARANTEED TOOL CALLS BENCHMARK")
    print("=" * 90)
    print("Using simple function that ALWAYS gets called (like official Agno example)")
    print(f"Running {len(BENCHMARK_QUERIES)} queries...")
    print("=" * 90)
    
    # Run both agents
    baseline_results = run_baseline_agent(BENCHMARK_QUERIES)
    optimized_results = run_optimized_agent(BENCHMARK_QUERIES, max_history_limit=3)
    
    # Calculate and display
    comparison = calculate_metrics(baseline_results, optimized_results)
    print_comparison_report(comparison)
    
    # Generate LinkedIn post
    linkedin_post = generate_linkedin_post(comparison)
    print("\n" + "=" * 90)
    print("📱 LINKEDIN POST")
    print("=" * 90)
    print(linkedin_post)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(f"benchmark_results_guaranteed_{timestamp}.json", 'w') as f:
        json.dump({'comparison': comparison}, f, indent=2)
    
    with open(f"linkedin_post_guaranteed_{timestamp}.txt", 'w') as f:
        f.write(linkedin_post)
    
    print(f"\n✅ Files saved with timestamp: {timestamp}")
    print("\n🎉 Benchmark complete with REAL savings!")


if __name__ == "__main__":
    main()
