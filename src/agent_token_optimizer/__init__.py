"""
Agent-Token-Optimizer: Sub-millisecond context compression and semantic deduplication engine.
Copyright (c) 2026 Benni OS Ecosystem. MIT Licensed.
"""

from .compressor import TokenCompressor, CompressionStats
from .json_squeezer import JSONSqueezer

__version__ = "0.1.0"
__all__ = ["TokenCompressor", "CompressionStats", "JSONSqueezer"]
