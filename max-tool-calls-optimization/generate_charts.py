"""
Generate visual charts for the benchmark comparison.
Creates publication-ready charts (300 DPI) showing token and cost savings.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import json
import sys

# Set style for professional charts
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {
    'baseline': '#FF6B6B',  # Red
    'optimized': '#4ECDC4',  # Teal
    'accent': '#FFE66D'     # Yellow
}


def create_tool_calls_comparison_chart(comparison, filename=None):
    """Create a bar chart comparing tool calls in context"""
    baseline = comparison['baseline']
    optimized = comparison['optimized']
    savings = comparison['savings']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Tool Calls\nin Context']
    baseline_vals = [baseline['tool_calls_in_context']]
    optimized_vals = [optimized['tool_calls_in_context']]
    
    x = range(len(categories))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], baseline_vals, width, 
                    label='Without Optimization', color=COLORS['baseline'], alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], optimized_vals, width,
                    label='With max_tool_calls_from_history=3', color=COLORS['optimized'], alpha=0.8)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_ylabel('Number of Tool Calls', fontsize=12, fontweight='bold')
    ax.set_title('Tool Calls in Context: Baseline vs Optimized', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend(fontsize=10)
    
    # Add savings annotation
    ax.text(0, max(baseline_vals) * 0.85, 
           f'{savings["tool_call_reduction_pct"]:.1f}% Reduction',
           ha='center', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor=COLORS['accent'], alpha=0.7))
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved: {filename}")
    else:
        plt.show()
    
    plt.close()


def create_token_cost_comparison_chart(comparison, filename=None):
    """Create a grouped bar chart comparing tokens and costs"""
    baseline = comparison['baseline']
    optimized = comparison['optimized']
    savings = comparison['savings']
    
    if not baseline['metrics'] or not optimized['metrics']:
        print("⚠️  No token metrics available, skipping token/cost chart")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Token comparison
    categories = ['Tokens']
    baseline_tokens = [baseline['metrics']['total_tokens']]
    optimized_tokens = [optimized['metrics']['total_tokens']]
    
    x = range(len(categories))
    width = 0.35
    
    bars1 = ax1.bar([i - width/2 for i in x], baseline_tokens, width,
                     label='Without Optimization', color=COLORS['baseline'], alpha=0.8)
    bars2 = ax1.bar([i + width/2 for i in x], optimized_tokens, width,
                     label='With Optimization', color=COLORS['optimized'], alpha=0.8)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax1.set_ylabel('Total Tokens', fontsize=12, fontweight='bold')
    ax1.set_title('Token Usage Comparison', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=11)
    ax1.legend(fontsize=9)
    
    # Add savings annotation
    ax1.text(0, max(baseline_tokens) * 0.75,
            f'{savings["token_savings_pct"]:.1f}% Savings',
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['accent'], alpha=0.7))
    
    # Cost comparison
    baseline_cost = (baseline['metrics']['input_tokens'] * 0.00015 + 
                    baseline['metrics']['output_tokens'] * 0.0006)
    optimized_cost = (optimized['metrics']['input_tokens'] * 0.00015 + 
                     optimized['metrics']['output_tokens'] * 0.0006)
    
    bars3 = ax2.bar([i - width/2 for i in x], [baseline_cost], width,
                     label='Without Optimization', color=COLORS['baseline'], alpha=0.8)
    bars4 = ax2.bar([i + width/2 for i in x], [optimized_cost], width,
                     label='With Optimization', color=COLORS['optimized'], alpha=0.8)
    
    # Add value labels
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.4f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax2.set_ylabel('Cost (USD)', fontsize=12, fontweight='bold')
    ax2.set_title('Cost Comparison (GPT-4o-mini)', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Cost'], fontsize=11)
    ax2.legend(fontsize=9)
    
    # Add savings annotation
    ax2.text(0, max([baseline_cost]) * 0.75,
            f'{savings["cost_savings_pct"]:.1f}% Savings',
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['accent'], alpha=0.7))
    
    plt.suptitle('Token & Cost Impact of max_tool_calls_from_history',
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved: {filename}")
    else:
        plt.show()
    
    plt.close()


def create_scaling_projection_chart(comparison, filename=None):
    """Create a line chart showing context growth projection"""
    baseline = comparison['baseline']
    optimized = comparison['optimized']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate average tool calls per query
    queries_count = 18  # From benchmark
    avg_tool_calls = baseline['tool_calls_total'] / queries_count
    max_limit = optimized['max_history_limit']
    
    # Project for up to 100 queries
    query_counts = list(range(0, 101, 5))
    baseline_context = [min(avg_tool_calls * q, avg_tool_calls * q) for q in query_counts]
    optimized_context = [min(avg_tool_calls * q, max_limit) for q in query_counts]
    
    # Plot lines
    ax.plot(query_counts, baseline_context, 'o-', linewidth=3, markersize=6,
            color=COLORS['baseline'], label='Without Optimization', alpha=0.8)
    ax.plot(query_counts, optimized_context, 's-', linewidth=3, markersize=6,
            color=COLORS['optimized'], label=f'With max_tool_calls_from_history={max_limit}', alpha=0.8)
    
    # Add horizontal line for max limit
    ax.axhline(y=max_limit, color=COLORS['optimized'], linestyle='--', 
               linewidth=2, alpha=0.5, label=f'Context Limit = {max_limit}')
    
    # Fill area between lines to show savings
    ax.fill_between(query_counts, baseline_context, optimized_context,
                     color=COLORS['accent'], alpha=0.3, label='Tokens Saved')
    
    ax.set_xlabel('Number of Queries', fontsize=13, fontweight='bold')
    ax.set_ylabel('Tool Calls in Context', fontsize=13, fontweight='bold')
    ax.set_title('Context Growth Over Time: Why max_tool_calls_from_history Matters',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Add annotations
    ax.annotate('Context explodes\nwithout limit!',
                xy=(80, baseline_context[-5]), xytext=(60, baseline_context[-5] + 20),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, fontweight='bold', color='red')
    
    ax.annotate('Context stays\nCONSTANT!',
                xy=(80, max_limit), xytext=(60, max_limit + 20),
                arrowprops=dict(arrowstyle='->', color=COLORS['optimized'], lw=2),
                fontsize=11, fontweight='bold', color=COLORS['optimized'])
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved: {filename}")
    else:
        plt.show()
    
    plt.close()


def load_latest_results():
    """Load the most recent benchmark results"""
    import glob
    import os
    
    # Find most recent results file
    result_files = glob.glob('benchmark_results_*.json')
    if not result_files:
        print("❌ No benchmark results found. Run benchmark_comparison.py first!")
        sys.exit(1)
    
    latest_file = max(result_files, key=os.path.getctime)
    print(f"📂 Loading results from: {latest_file}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    return data['comparison']


def main():
    """Generate all charts from benchmark results"""
    print("\n📊 GENERATING BENCHMARK CHARTS")
    print("=" * 70 + "\n")
    
    # Load results
    comparison = load_latest_results()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate all charts
    print("\n🎨 Creating charts...")
    
    create_tool_calls_comparison_chart(
        comparison, 
        f"chart_tool_calls_{timestamp}.png"
    )
    
    create_token_cost_comparison_chart(
        comparison,
        f"chart_token_cost_{timestamp}.png"
    )
    
    create_scaling_projection_chart(
        comparison,
        f"chart_scaling_{timestamp}.png"
    )
    
    print("\n" + "=" * 70)
    print("✅ All charts generated successfully!")
    print("=" * 70)
    print("\n💡 TIP: Use these charts in your LinkedIn post for maximum impact!")
    print("   The charts are publication-ready at 300 DPI.\n")


if __name__ == "__main__":
    main()
