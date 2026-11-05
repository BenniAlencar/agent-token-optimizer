"""
Unit tests for JSONSqueezer.
"""

import unittest
import json
from agent_token_optimizer.json_squeezer import JSONSqueezer

class TestJSONSqueezer(unittest.TestCase):
    def test_prune_empty_nodes(self):
        raw = json.dumps({
            "name": "Benni",
            "empty_list": [],
            "empty_dict": {},
            "null_field": None,
            "nested": {
                "active": True,
                "blank": ""
            }
        }, indent=2)
        
        compact, reduction = JSONSqueezer.squeeze(raw)
        data = json.loads(compact)
        self.assertNotIn("empty_list", data)
        self.assertNotIn("null_field", data)
        self.assertNotIn("blank", data["nested"])
        self.assertEqual(data["name"], "Benni")
        self.assertGreater(reduction, 50.0)
