# Response Caching Demo

**Save 80%+ on API costs during development** by caching model responses locally.

## What This Demonstrates

Response caching stores model responses locally to avoid redundant API calls during development and testing. This demo shows real-world impact across different scenarios.

### Key Benefits

- 🚀 **5-10x faster** iteration cycles
- 💰 **70-90% cost reduction** during development
- ⚡ **Instant responses** for repeated queries
- 🧪 **Consistent outputs** for testing

## Quick Start

### Prerequisites

```bash
pip install agno openai
export OPENAI_API_KEY=your_key_here
```

### Run the Demos

**1. Simple Side-by-Side Comparison** (30 seconds)
```bash
python simple_comparison.py
```

Shows immediate impact: 5 identical queries with vs without caching.

**2. Full Development Day Simulation** (2-3 minutes)
```bash
python full_day_simulation.py
```

Simulates a realistic 8-hour development workflow with 50 test iterations.

## Demo Results

### Simple Comparison
```
🔴 WITHOUT CACHING:
  Run 1... 2.34s
  Run 2... 4.82s
  Run 3... 7.15s
  Run 4... 9.58s
  Run 5... 11.97s
  Total: 11.97s | Cost: $0.0025

🟢 WITH CACHING:
  Run 1... 2.31s 📡 API call
  Run 2... 2.32s ✨ CACHED!
  Run 3... 2.32s ✨ CACHED!
  Run 4... 2.32s ✨ CACHED!
  Run 5... 2.32s ✨ CACHED!
  Total: 2.32s | Cost: $0.0005

📊 IMPACT:
⚡ 5.2x faster
💵 80% cost reduction
⏰ 9.65 seconds saved
```

### Full Day Simulation
```
📅 50 test iterations across the day

🟢 WITH CACHING:
  Only 3 API calls (one per unique query)
  47 cache hits (94% hit rate)
  
💡 SAVINGS:
⚡ ~90 seconds saved
💵 ~$0.08 saved (85% reduction)
📞 47 fewer API calls
```

## How It Works

### Basic Usage

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Enable caching with one parameter
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o",
        cache_response=True  # That's it!
    )
)

# First call hits API
agent.run("Your query")

# Second identical call is instant!
agent.run("Your query")
```

### Configuration Options

```python
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o",
        cache_response=True,
        cache_ttl=3600,  # Expire after 1 hour
        cache_dir="./my_cache"  # Custom location
    )
)
```

## Use Cases

### ✅ Perfect For

- **Development iterations** - Testing same queries while tweaking code
- **Unit testing** - Consistent responses across test runs
- **Debugging** - Reproduce exact responses
- **Demos** - Ensure polished, rehearsed outputs
- **Rate limit management** - Reduce API call volume

### ❌ Not For

- **Production** - Users expect fresh responses
- **Real-time data** - Stock prices, weather, news
- **Personalized content** - Each user needs unique answers

## Technical Details

### Cache Key Generation

Cache keys are based on:
- Model ID
- Message content and roles
- Tools available
- Response format

- Streaming vs non-streaming

### Storage Location

Default: `~/.agno/cache/model_responses`

Caches persist across sessions and program restarts.

## ROI Calculator

**Example: Building an agent with 100 test iterations/day**

Without Caching:
- 100 iterations × $0.002/call = **$0.20/day**
- 100 iterations × 2s/call = **3.3 minutes/day**

With Caching (assuming 80% hit rate):
- 20 API calls × $0.002 = **$0.04/day**
- 20 × 2s + 80 × 0.01s = **41 seconds/day**

**Monthly Savings (20 work days):**
- 💵 $3.20/month in API costs
- ⏰ 50 minutes/month in waiting time

*Scales significantly with larger teams and more iterations*

## Related Demos

- [Max Tool Calls Optimization](../max-tool-calls-optimization/) - Reduce context size by 70%+

## Resources

- [Response Caching Docs](https://docs.agno.com/concepts/models/cache-response)
- [Agno GitHub](https://github.com/agno-agi/agno)
- [Model Configuration](https://docs.agno.com/concepts/models/overview)

## Contributing

Have ideas to improve this demo? Open a PR or issue in the [agno-demo repo](https://github.com/agno-agi/agno-demo).

## License

MIT - See main repo for details.
