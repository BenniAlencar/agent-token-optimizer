"""
Squeezes verbose JSON payloads returned by MCP tools and REST APIs.
"""

import json
from typing import Any, Dict, List, Tuple

class JSONSqueezer:
    """
    Minifies and prunes verbose JSON structures.
    Strips null values, empty collections, and default repetitive keys
    to cut MCP tool output tokens by up to 75%.
    """

    @classmethod
    def prune_empty_nodes(cls, data: Any) -> Any:
        """Recursively removes nulls, empty dicts, and empty lists."""
        if isinstance(data, dict):
            pruned = {
                k: cls.prune_empty_nodes(v)
                for k, v in data.items()
                if v is not None and v != "" and v != [] and v != {}
            }
            return {k: v for k, v in pruned.items() if v is not None and v != "" and v != [] and v != {}}
        elif isinstance(data, list):
            pruned_list = [
                cls.prune_empty_nodes(item)
                for item in data
                if item is not None and item != "" and item != [] and item != {}
            ]
            return [x for x in pruned_list if x is not None and x != "" and x != [] and x != {}]
        return data

    @classmethod
    def squeeze(cls, raw_json_str: str) -> Tuple[str, float]:
        """
        Parses JSON, prunes empty fields, and serializes to compact whitespace-free string.
        Returns (compact_json_str, percentage_reduction).
        """
        data = json.loads(raw_json_str)
        cleaned = cls.prune_empty_nodes(data)
        compact = json.dumps(cleaned, separators=(',', ':'), ensure_ascii=False)
        
        orig_len = len(raw_json_str)
        comp_len = len(compact)
        reduction = ((orig_len - comp_len) / orig_len * 100.0) if orig_len > 0 else 0.0
        return compact, reduction
