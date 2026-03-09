#!/usr/bin/env python3
"""Push an agent's state to Star Office UI. Usage: python3 push-agent-state.py <agentId> <joinKey> <state> [detail]"""
import sys, json, urllib.request

OFFICE_URL = "http://127.0.0.1:19000"

AGENT_IDS = {
    "zeus": ("agent_1773018779855_n8fm", "ocj_zeus_temple"),
    "atum": ("agent_1773018779856_xufo", "ocj_atum_temple"),
    "athena": ("agent_1773018779857_3pau", "ocj_athena_temple"),
    "maat": ("agent_1773018779857_k5w1", "ocj_maat_temple"),
    "sphinx": ("agent_1773018779858_7ig7", "ocj_sphinx_temple"),
    "ibis": ("agent_1773018779859_1hyb", "ocj_ibis_temple"),
    "hathor": ("agent_1773018779859_8g47", "ocj_hathor_temple"),
    "osiris": ("agent_1773018779860_2416", "ocj_osiris_temple"),
}

if len(sys.argv) < 3:
    print("Usage: python3 push-agent-state.py <agentName> <state> [detail]")
    print("States: idle | writing | researching | executing | syncing | error")
    print("Agents:", ", ".join(AGENT_IDS.keys()))
    sys.exit(1)

agent_name = sys.argv[1].lower()
state = sys.argv[2]
detail = sys.argv[3] if len(sys.argv) > 3 else ""

if agent_name not in AGENT_IDS:
    print(f"Unknown agent: {agent_name}. Known: {list(AGENT_IDS.keys())}")
    sys.exit(1)

agent_id, join_key = AGENT_IDS[agent_name]

payload = json.dumps({
    "agentId": agent_id,
    "joinKey": join_key,
    "state": state,
    "detail": detail
}).encode()

req = urllib.request.Request(f"{OFFICE_URL}/agent-push",
                              data=payload,
                              headers={"Content-Type": "application/json"},
                              method="POST")
with urllib.request.urlopen(req) as r:
    resp = json.loads(r.read().decode())
    print(f"Updated {agent_name}: {state} — {detail} -> {resp}")
