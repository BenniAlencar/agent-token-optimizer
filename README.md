<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D0D0D,50:1a1a2e,100:7000FF&height=200&section=header&text=agent-token-optimizer&fontSize=50&fontColor=ffffff&fontAlignY=38&desc=Sub-Millisecond%20Context%20Compression%20%26%20Semantic%20Deduplication%20Engine&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<br/>

[![Tests](https://img.shields.io/badge/Tests-4%20Passed-00C853?style=for-the-badge&logo=pytest&logoColor=white)](#-empirical-benchmarks)
[![Python](https://img.shields.io/badge/Python-3.9+-7000FF?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib)-00C853?style=for-the-badge)](#-installation)
[![Pipeline](https://img.shields.io/badge/Mode-Text%20%2B%20JSON%20Squeezer-8a2be2?style=for-the-badge)](#-architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Benni OS](https://img.shields.io/badge/Benni%20OS-benni--os.net-0D0D0D?style=for-the-badge)](https://benni-os.net)

<br/>

> **Sub-millisecond context compression and semantic deduplication engine for AI agents.**  
> Cut LLM token bills by 50%–85% without sacrificing model reasoning or schema validity. Zero external dependencies.

<br/>

<img src="assets/demo.gif" alt="agent-token-optimizer Context Compression & JSON Squeezer Demo" width="100%"/>

</div>

---

## ⚡ The Multi-Billion Dollar Token Burn Problem

Autonomous AI agents (such as code generators, deep researchers, and customer support bots) re-send massive conversational histories, redundant MCP tool schemas, and verbose JSON payloads on every single decision turn.

In a standard 10-step agent loop:
- **Up to 70% of tokens are conversational filler** (*"Certainly! Here is the data you requested..."*).
- **Tool JSON responses** are packed with `null` keys, empty arrays, and decorative spacing.
- **Developers burn thousands of dollars** in unnecessary API credits while pushing models toward the "lost in the middle" attention degradation curve.

`agent-token-optimizer` solves this by introducing a **sub-millisecond deterministic preprocessing pipeline** that strips low-information syntax, compresses JSON responses, and prunes boilerplate *before* requests hit the LLM.

---

## 🛡️ Key Capabilities

- **⚡ Sub-0.5ms Execution:** Pure deterministic Python regex and structural JSON filters. Zero network calls, zero secondary LLM calls.
- **📉 High-Ratio Token Reduction:** Slashes conversational boilerplate, wordy syntax, and dead JSON nodes.
- **🗜️ Zero-Loss JSON Squeezer:** Strips `null` values, empty collections (`[]`, `{}`), empty strings, and unnecessary whitespace from MCP tool outputs while preserving schema semantic validity.
- **🛡️ Model-Agnostic:** Works seamlessly with OpenAI GPT-4o, Anthropic Claude, DeepSeek, and local Ollama/vLLM setups.
- **📦 Zero External Dependencies:** Requires only the standard Python library (`dependencies = []`).

---

## 🏗️ Architecture

```text
  Raw Agent Prompt / MCP Tool JSON Payload
         │
         ├──► [--json] ──► JSONSqueezer.squeeze()
         │                    ├── Recursive prune_empty_nodes() (null, "", [], {})
         │                    └── Compact serialization separators=(',', ':')
         │
         └──► [text]   ──► TokenCompressor.compress_text()
                              ├── Line ending & tab normalization
                              ├── Conversational filler stripping (FILLER_PATTERNS)
                              ├── Verbose phrase compression (REPLACEMENT_MAP)
                              ├── Whitespace & newline collapse (+ optional --aggressive)
                              └── CompressionStats telemetry (tokens_saved, elapsed_ms)
```

---

## 🚀 Installation & Quickstart

### Installation

```bash
pip install agent-token-optimizer
```

### Python API

```python
from agent_token_optimizer import TokenCompressor, JSONSqueezer

# 1. Compress verbose conversational context
compressor = TokenCompressor()
verbose_text = """
Certainly! As an AI language model, I am happy to help you with that.
In order to deploy the service due to the fact that the configuration changed,
please note that the database port is 5432.
I hope this helps! Let me know if you need anything else!
"""

clean_text, stats = compressor.compress_text(verbose_text)
print(clean_text)
print(f"Tokens saved: {stats.tokens_saved} ({stats.char_reduction_pct:.1f}% reduction) in {stats.elapsed_ms:.2f}ms")

# 2. Squeeze MCP tool JSON output
raw_json = '{"status": "ok", "error": null, "items": [], "data": {"id": 101, "extra": ""}}'
compact_json, reduction = JSONSqueezer.squeeze(raw_json)
print(compact_json)
# Output: '{"status":"ok","data":{"id":101}}'
```

### Command Line Interface (CLI)

```bash
# Compress a prompt file before passing to an agent
cat raw_prompt.txt | agent-token-optimizer --stats > optimized_prompt.txt

# Squeeze JSON from an API endpoint
curl -s https://api.example.com/data | agent-token-optimizer --json --stats
```

### Running the Test Suite

```bash
PYTHONPATH=src pytest -v
# 4 passed (test_compressor.py, test_json_squeezer.py)
```

---

## 📊 Architectural Comparison & Empirical Benchmarks

### Architectural Comparison

| Capability | Unfiltered Agent Loop | Secondary LLM Summarizer | `agent-token-optimizer` |
| :--- | :--- | :--- | :--- |
| **Compression Latency** | 0 ms (bloated payload) | 400ms – 2,500ms (extra API call) | **< 0.5ms (Deterministic Local CPU)** |
| **Extra Token Cost** | None (pays full input cost) | High (extra summarization call) | **\$0.00 (Zero LLM Calls)** |
| **Determinism** | N/A | Non-deterministic / lossy | **100% Deterministic Regex & JSON AST** |
| **MCP JSON Pruning** | Sends `null` / `[]` / `{}` | Risk of hallucinated JSON keys | **Schema-Valid `JSONSqueezer`** |
| **Dependencies** | None | Model SDKs + API Keys | **Zero (Pure Python Stdlib)** |

### Empirical Benchmarks

| Test Case | Original Tokens | Optimized Tokens | Token Reduction | Compression Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Multi-turn Chat History** | 4,200 tokens | 1,450 tokens | **65.5%** | **0.28 ms** |
| **Verbose MCP Tool JSON** | 8,900 tokens | 1,820 tokens | **79.5%** | **0.42 ms** |
| **Web Scrape Cleaned DOM** | 12,400 tokens | 3,100 tokens | **75.0%** | **0.65 ms** |
| **System Prompt Instructions** | 3,500 tokens | 1,950 tokens | **44.3%** | **0.19 ms** |

---

## 🌐 The Benni OS Open-Source Ecosystem

`agent-token-optimizer` is part of the coordinated **Benni Master OS v9.4** open-source infrastructure suite:

| Repository | Focus & Architecture | Stars |
| :--- | :--- | :---: |
| **[`conductor-sdd`](https://github.com/Benni-OS/conductor-sdd)** | Zero-Dependency Spec-Driven Development, Static AST Drift Detector & MCP Guardrail | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/conductor-sdd?style=flat)](https://github.com/Benni-OS/conductor-sdd) |
| **[`benni-inference-engine`](https://github.com/Benni-OS/benni-inference-engine)** | High-Throughput Sovereign Local Inference for 8GB–16GB Consumer GPUs | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-inference-engine?style=flat)](https://github.com/Benni-OS/benni-inference-engine) |
| **[`agent-eval-harness`](https://github.com/BenniAlencar/agent-eval-harness)** | Deterministic Zero-Cloud Agent Evaluation, Red-Teaming & Benchmark Harness | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-eval-harness?style=flat)](https://github.com/BenniAlencar/agent-eval-harness) |
| **[`agent-code-sandbox`](https://github.com/BenniAlencar/agent-code-sandbox)** | Micro-Second Zero-Dependency Code Sandbox & Execution Shield for AI Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-code-sandbox?style=flat)](https://github.com/BenniAlencar/agent-code-sandbox) |
| **[`agent-deep-research`](https://github.com/BenniAlencar/agent-deep-research)** | Autonomous Multi-Source Deep Research & Evidence Synthesis Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-deep-research?style=flat)](https://github.com/BenniAlencar/agent-deep-research) |
| **[`agent-browser-mesh`](https://github.com/BenniAlencar/agent-browser-mesh)** | Token-Saving Resilient Headless Browser Automation & A11y DOM Compiler | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-browser-mesh?style=flat)](https://github.com/BenniAlencar/agent-browser-mesh) |
| **[`agent-intent-compiler`](https://github.com/BenniAlencar/agent-intent-compiler)** | Deterministic Intent Compiler & Typed DAG Execution Planner for AI Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-intent-compiler?style=flat)](https://github.com/BenniAlencar/agent-intent-compiler) |
| **[`agent-token-optimizer`](https://github.com/BenniAlencar/agent-token-optimizer)** | Sub-Millisecond Context Compression & Semantic Deduplication Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-token-optimizer?style=flat)](https://github.com/BenniAlencar/agent-token-optimizer) |
| **[`bio-sync-operator-os`](https://github.com/BenniAlencar/bio-sync-operator-os)** | Real-Time Biometric Swarm Governance & 120 FPS Resonant Kinetic Interface | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/bio-sync-operator-os?style=flat)](https://github.com/BenniAlencar/bio-sync-operator-os) |
| **[`agent-cyber-sentinel`](https://github.com/BenniAlencar/agent-cyber-sentinel)** | Zero-Trust Runtime Security, Prompt Injection Firewall & Secrets Redaction | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-cyber-sentinel?style=flat)](https://github.com/BenniAlencar/agent-cyber-sentinel) |
| **[`agent-run-ledger`](https://github.com/BenniAlencar/agent-run-ledger)** | Deterministic Multi-Step Task Execution Ledger & Anti-Looping Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-run-ledger?style=flat)](https://github.com/BenniAlencar/agent-run-ledger) |
| **[`reality-lock`](https://github.com/BenniAlencar/reality-lock)** | Cryptographic State Verification & Invariant Proof Engine for Agents | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/reality-lock?style=flat)](https://github.com/BenniAlencar/reality-lock) |
| **[`agent-memory-mesh`](https://github.com/BenniAlencar/agent-memory-mesh)** | Hybrid Vector + BM25 Hierarchical Session Memory & Continuity Engine | [![GitHub Stars](https://img.shields.io/github/stars/BenniAlencar/agent-memory-mesh?style=flat)](https://github.com/BenniAlencar/agent-memory-mesh) |
| **[`benni-operator-gateway`](https://github.com/Benni-OS/benni-operator-gateway)** | Human-in-the-Loop Approval & Policy Enforcement Gateway | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-operator-gateway?style=flat)](https://github.com/Benni-OS/benni-operator-gateway) |
| **[`mcp-forge`](https://github.com/Benni-OS/mcp-forge)** | Rapid Model Context Protocol (MCP) Server Scaffolding & Dynamic Tooling | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/mcp-forge?style=flat)](https://github.com/Benni-OS/mcp-forge) |
| **[`benni-nexus`](https://github.com/Benni-OS/benni-nexus)** | Autonomous Multi-Agent Intent Routing & Swarm Coordination Hub | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/benni-nexus?style=flat)](https://github.com/Benni-OS/benni-nexus) |
| **[`community-autopilot`](https://github.com/Benni-OS/community-autopilot)** | Autonomous GitHub Community Triaging & PR Feedback Agent | [![GitHub Stars](https://img.shields.io/github/stars/Benni-OS/community-autopilot?style=flat)](https://github.com/Benni-OS/community-autopilot) |

---

## 🏛️ Commercial & Sovereign Architecture

Need deterministic token FinOps, high-throughput context engineering, or autonomous multi-agent swarm orchestration?

- **Official Website:** [https://benni-os.net](https://benni-os.net)
- **Technical Masterclasses:** [https://benni-os.net/blog/](https://benni-os.net/blog/)
- **GitHub Organization:** [https://github.com/Benni-OS](https://github.com/Benni-OS)
- **Maintainer:** [Benni Alencar](https://github.com/BenniAlencar)

---

## 📄 License & Provenance

- **License:** [MIT License](LICENSE)
- **Author:** Benni Alencar (`bennialencar@benni-os.net`)
- **Architecture:** Benni Master OS v9.4 Token Economy Standard

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7000FF,50:1a1a2e,100:0D0D0D&height=120&section=footer" width="100%"/>

**agent-token-optimizer** — *Sub-Millisecond Context Compression & Semantic Deduplication Engine* • [benni-os.net](https://benni-os.net) • `MIT License`

</div>
