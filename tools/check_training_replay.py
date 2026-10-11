"""Offline synthetic instructor-contract checks; no aircraft physics or I/O adapters."""
import argparse
import hashlib
import json
from pathlib import Path


class ContractError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def validate_manifest(m):
    required = {"schema_version", "scenario_id", "revision", "seed", "execution_profile",
                "dynamics_owner", "frame", "units", "tick_s", "initial_state",
                "allowed_cues", "required_acknowledgements", "expected_actions"}
    if set(m) != required:
        raise ContractError("Manifest fields do not match v1 contract")
    if (m["schema_version"] != "1.0" or m["execution_profile"] != "synthetic-contract"
            or m["frame"] != "ENU" or m["units"] != "SI"
            or m["dynamics_owner"] != "scripted-source"):
        raise ContractError("Unsupported version/profile/frame/units/owner")
    if (not isinstance(m["scenario_id"], str) or not m["scenario_id"]
            or not isinstance(m["revision"], str) or not m["revision"]
            or type(m["seed"]) is not int or type(m["tick_s"]) is not int
            or m["tick_s"] <= 0):
        raise ContractError("Invalid identity, seed or tick")
    if m["initial_state"] != {"sim_time_s": 0, "visibility": "baseline"}:
        raise ContractError("Unsupported initial state")
    for field in ("allowed_cues", "required_acknowledgements", "expected_actions"):
        values = m[field]
        if not isinstance(values, list) or not all(isinstance(v, str) and v for v in values):
            raise ContractError("Invalid manifest list: " + field)
    if (len(set(m["allowed_cues"])) != len(m["allowed_cues"])
            or len(set(m["required_acknowledgements"])) != len(m["required_acknowledgements"])
            or not set(m["required_acknowledgements"]) <= set(m["allowed_cues"])):
        raise ContractError("Invalid cue requirements")
    actions = {"ready", "start", "pause", "resume", "reset", "stop", "step",
               "inject_cue", "acknowledge"}
    if not m["expected_actions"] or not set(m["expected_actions"]) <= actions:
        raise ContractError("Invalid expected action sequence")


def replay(manifest, log):
    validate_manifest(manifest)
    if set(log) != {"manifest_sha256", "events", "expected_summary"}:
        raise ContractError("Invalid log envelope")
    if log["manifest_sha256"] != digest(manifest):
        raise ContractError("Manifest checksum mismatch")
    if not isinstance(log["events"], list):
        raise ContractError("Events must be a list")
    state, sim_time, episode = "configured", 0, 0
    active, acknowledged, ids, trace, actions = set(), set(), set(), [], []
    transitions = {"ready": ("configured", "ready"), "start": ("ready", "running"),
                   "pause": ("running", "paused"), "resume": ("paused", "running")}
    for seq, event in enumerate(log["events"], 1):
        if not isinstance(event, dict) or set(event) != {
                "event_id", "sequence", "episode", "sim_time_s", "producer", "action", "payload"}:
            raise ContractError("Invalid event fields")
        eid, action, payload = event["event_id"], event["action"], event["payload"]
        if not isinstance(eid, str) or not eid or eid in ids:
            raise ContractError("Missing or duplicate event ID")
        ids.add(eid)
        if (type(event["sequence"]) is not int or event["sequence"] != seq
                or type(event["episode"]) is not int or event["episode"] != episode
                or type(event["sim_time_s"]) is not int or event["sim_time_s"] != sim_time):
            raise ContractError("Sequence, episode or simulation timestamp mismatch")
        if not isinstance(payload, dict):
            raise ContractError("Payload must be an object")
        owner = "scripted-source" if action == "step" else "trainee" if action == "acknowledge" else "instructor"
        if event["producer"] != owner:
            raise ContractError("Control authority violation")
        if action in transitions:
            before, after = transitions[action]
            if state != before or payload:
                raise ContractError("Invalid lifecycle transition")
            state = after
        elif action == "step":
            if (state != "running" or payload != {"dt_s": manifest["tick_s"]}
                    or type(payload.get("dt_s")) is not int):
                raise ContractError("Invalid step; pause freezes simulation time")
            sim_time += manifest["tick_s"]
        elif action == "inject_cue":
            if (state not in {"running", "paused"} or set(payload) != {"cue"}
                    or payload["cue"] not in manifest["allowed_cues"]
                    or payload["cue"] in active):
                raise ContractError("Invalid or duplicate instructor cue")
            active.add(payload["cue"])
        elif action == "acknowledge":
            if (state != "running" or set(payload) != {"cue"}
                    or payload["cue"] not in active or payload["cue"] in acknowledged):
                raise ContractError("Invalid trainee acknowledgement")
            acknowledged.add(payload["cue"])
        elif action == "reset":
            if state not in {"paused", "stopped"} or payload:
                raise ContractError("Reset requires paused or stopped state")
            state, sim_time, episode = "ready", 0, episode + 1
            active, acknowledged = set(), set()
        elif action == "stop":
            if state not in {"running", "paused"} or payload:
                raise ContractError("Invalid stop")
            state = "stopped"
        else:
            raise ContractError("Unknown action")
        actions.append(action)
        trace.append({"sequence": seq, "state": state, "sim_time_s": sim_time,
                      "episode": episode, "active_cues": sorted(active),
                      "acknowledged_cues": sorted(acknowledged)})
    if actions != manifest["expected_actions"] or state != "stopped":
        raise ContractError("Incomplete or unexpected scenario sequence")
    summary = {"scenario_id": manifest["scenario_id"], "revision": manifest["revision"],
               "events": len(trace), "episode": episode, "state": state,
               "sim_time_s": sim_time, "acknowledged_cues": sorted(acknowledged),
               "objective_met": set(manifest["required_acknowledgements"]) <= acknowledged,
               "trace_sha256": digest(trace)}
    if summary != log["expected_summary"]:
        raise ContractError("Replay differs from expected debrief")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    try:
        result = replay(json.loads(args.manifest.read_text()), json.loads(args.log.read_text()))
    except (ContractError, ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, "Replay rejected: " + str(exc) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
