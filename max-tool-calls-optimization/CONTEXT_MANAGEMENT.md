# Managing Tool Calls in Context

Official Documentation: https://docs.agno.com/concepts/agents/context#managing-tool-calls

## Overview

In multi-turn agent conversations with tool-calling, conversation history can grow exponentially as every tool call and result is stored in context. This leads to:

- Increased token usage
- Higher API costs
- Potential context limit issues
- Reduced performance

## Solution: max_tool_calls_from_history

The `max_tool_calls_from_history` parameter limits how many historical tool calls are kept in context.

### Feature Details

Added in Agno v2.2.0 (Release Notes: https://github.com/agno-agi/agno/releases)

**Description**: Filter tool calls from history by loading a fixed number of tool calls from history. Helps manage context size and reduce tokens.

### Usage

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    max_tool_calls_from_history=3,  # Only keep 3 most recent tool calls
    add_history_to_context=True,
)
```

### Key Parameters

- `max_tool_calls_from_history` (int): Maximum number of tool calls to keep from history
- `add_history_to_context` (bool): Must be set to True to enable history

### Benefits

1. **Constant Context Size**: Context doesn't grow with conversation length
2. **Cost Reduction**: 70-90% reduction in token usage for long conversations
3. **Scalability**: Agents can handle unlimited conversation length
4. **Performance**: Faster processing with smaller context windows

### Recommended Values

- **3-5**: Good for most use cases
- **1-2**: Ultra-minimal context, fastest performance
- **10+**: When you need more historical tool context

### Related Parameters

- `num_history_runs` (int): Limits number of history responses (not tool calls)
- `add_history_to_context` (bool): Enable/disable history in context

## Context Management Best Practices

1. Start with `max_tool_calls_from_history=3` and adjust based on needs
2. Monitor token usage and costs
3. Use `num_history_runs` to limit conversation history responses
4. Combine with session storage for long-running agents
5. Consider using memory for important context retention

## Additional Resources

- [Context Engineering Documentation](https://docs.agno.com/concepts/agents/context)
- [Sessions Documentation](https://docs.agno.com/concepts/agents/sessions)
- [Memory Documentation](https://docs.agno.com/concepts/agents/memory)
- [Agent Reference](https://docs.agno.com/reference/agents/agent)

## Release Information

Feature added in Agno v2.2.0 (October 2024)

GitHub Release: https://github.com/agno-agi/agno/releases/tag/v2.2.0
