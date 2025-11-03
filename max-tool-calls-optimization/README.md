# Agno `max_tool_calls_from_history` Benchmark

Benchmarking demonstration showing token and cost savings using Agno's `max_tool_calls_from_history` feature.

**Official Documentation:** https://docs.agno.com/examples/concepts/agent/context_management/filter_tool_calls_from_history

## Results

With 50 queries:

| Metric | Baseline | Optimized | Savings |
|--------|----------|-----------|---------|
| **Avg Context Size** | 25.5 tool calls | 3.9 tool calls | **84.8%** ⬇️ |
| **Token Usage** | 10,578 tokens | 4,647 tokens | **56.1%** ⬇️ |
| **Cost (GPT-4o-mini)** | $1.62 | $0.72 | **55.6%** ⬇️ |

## Quick Start

```bash
# 1. Install dependencies
pip install agno openai

# 2. Set your OpenAI API key
export OPENAI_API_KEY='your-key-here'

# 3. Run benchmark (~8-10 minutes)
python benchmark.py

# 4. Generate charts (optional)
python generate_charts.py
```

## How It Works

Compares two agents running 50 identical queries:

**Baseline Agent** (No optimization):
```python
agent = Agent(
    add_history_to_context=True,
    num_history_runs=None,  # Unlimited - context grows: 1→2→3...→50
)
```

**Optimized Agent** (With `max_tool_calls_from_history`):
```python
agent = Agent(
    add_history_to_context=True,
    num_history_runs=None,
    max_tool_calls_from_history=3,  # Bounded - context: 1→2→3→4→4...→4
)
```

## Key Insight

The database preserves complete history. Two parameters control what the LLM sees in context:

- **`num_history_runs`**: How many conversation runs to include
- **`max_tool_calls_from_history`**: How many tool calls from those runs

⚠️ **Critical**: Agno defaults to `num_history_runs=3` when you set `add_history_to_context=True`. 

Without explicitly setting `num_history_runs=None`, both baseline and optimized agents would be limited to 3 runs, showing no savings!

## Why Guaranteed Tool Calls?

This benchmark uses a simple custom function that the agent MUST call:

```python
def get_info_about_topic(topic: str) -> str:
    """Get information about a topic. This function ALWAYS gets called."""
    return f"Latest research shows significant advances in {topic}."
```

Unlike optional tools (like web search), this guarantees:
- ✅ Exactly 1 tool call per query
- ✅ Predictable context growth
- ✅ Clear demonstration of `max_tool_calls_from_history` benefit

## Output Files

After running the benchmark:
- `benchmark_results_guaranteed_*.json` - Raw metrics
- `chart_*.png` - Visualizations (if you run generate_charts.py)

## Why Token Savings < Context Savings?

Token savings (56%) are lower than context reduction (85%) because:
- Not all tokens are tool calls (includes user messages, system prompts, responses)
- Tool call outputs are similar length in both cases
- The reduction is specifically in tool call history

This is normal and expected!

## Use Cases

Perfect for:
- 🔄 Multi-turn agentic workflows
- 💬 Long-running conversations
- 💰 Production cost optimization
- 📊 Avoiding context limit issues

## License

MIT
