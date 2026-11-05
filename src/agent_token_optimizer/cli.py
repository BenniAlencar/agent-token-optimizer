"""
Command line interface for Agent-Token-Optimizer.
"""

import sys
import argparse
from .compressor import TokenCompressor
from .json_squeezer import JSONSqueezer

def main():
    parser = argparse.ArgumentParser(description="Agent-Token-Optimizer: Context compression CLI")
    parser.add_argument("input", nargs="?", help="Text to compress, or path to file")
    parser.add_argument("--json", action="store_true", help="Compress as JSON payload")
    parser.add_argument("--aggressive", action="store_true", help="Enable aggressive compression")
    parser.add_argument("--stats", action="store_true", help="Print compression statistics to stderr")
    
    args = parser.parse_args()

    content = ""
    if args.input:
        import os
        if os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.input
    else:
        content = sys.stdin.read()

    if not content:
        sys.exit(0)

    if args.json:
        compact, red = JSONSqueezer.squeeze(content)
        sys.stdout.write(compact + "\n")
        if args.stats:
            sys.stderr.write(f"[JSON Squeezer] Reduction: {red:.1f}%\n")
    else:
        compressor = TokenCompressor(aggressive=args.aggressive)
        compressed, stats = compressor.compress_text(content)
        sys.stdout.write(compressed + "\n")
        if args.stats:
            sys.stderr.write(
                f"[Token Compressor] Reduced by {stats.char_reduction_pct:.1f}% "
                f"({stats.est_original_tokens} -> {stats.est_compressed_tokens} tokens) "
                f"in {stats.elapsed_ms:.2f}ms\n"
            )

if __name__ == "__main__":
    main()
