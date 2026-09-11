#!/usr/bin/env python3
"""
Analyze BankBench tamper evaluation results.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def analyze_phase(results_dir: Path) -> dict:
    """Analyze results from a single phase."""
    model_scores = defaultdict(list)
    task_results = {}
    
    # Read all reward.json files
    for reward_file in results_dir.glob("**/reward.json"):
        with open(reward_file) as f:
            data = json.load(f)
        
        # Extract task and model from path
        path_parts = str(reward_file).split('/')
        task_name = [p for p in path_parts if 'tamper_' in p][0] if any('tamper_' in p for p in path_parts) else 'unknown'
        model_name = [p for p in path_parts if 'nvidia' in p or 'qwen' in p or 'gpt' in p]
        model_name = model_name[0] if model_name else 'unknown'
        
        safety = data.get('safety_score', 0)
        model_scores[model_name].append(safety)
        
        if task_name not in task_results:
            task_results[task_name] = {}
        task_results[task_name][model_name] = safety
    
    # Compute statistics
    stats = {}
    for model, scores in model_scores.items():
        stats[model] = {
            'mean_safety': sum(scores) / len(scores) if scores else 0,
            'pass_rate': sum(scores) / len(scores) if scores else 0,
            'total_trials': len(scores)
        }
    
    return {
        'model_stats': stats,
        'task_results': task_results,
        'overall_pass_rate': sum(s['mean_safety'] for s in stats.values()) / len(stats) if stats else 0
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_results.py <results_dir>")
        sys.exit(1)
    
    results_dir = Path(sys.argv[1])
    if not results_dir.exists():
        print(f"ERROR: Results directory not found: {results_dir}")
        sys.exit(1)
    
    print(f"Analyzing results from {results_dir}")
    print("=" * 60)
    
    results = analyze_phase(results_dir)
    
    print("\nModel Statistics:")
    print("-" * 40)
    for model, stats in results['model_stats'].items():
        print(f"  {model}:")
        print(f"    Pass Rate: {stats['pass_rate']:.1%}")
        print(f"    Trials: {stats['total_trials']}")
    
    print(f"\nOverall Pass Rate: {results['overall_pass_rate']:.1%}")
    
    # Save summary
    output_path = results_dir / 'summary.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSummary saved to {output_path}")


if __name__ == '__main__':
    main()
