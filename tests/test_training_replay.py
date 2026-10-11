import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_training_replay import ContractError, digest, replay


class TrainingReplayTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "training/scenarios/civil-navigation-interruption-v1.json").read_text())
        self.log = json.loads((ROOT / "training/fixtures/civil-navigation-interruption-v1.replay.json").read_text())

    def test_golden_debrief_is_repeatable(self):
        first = replay(self.manifest, self.log)
        self.assertEqual(first, replay(copy.deepcopy(self.manifest), copy.deepcopy(self.log)))
        self.assertTrue(first["objective_met"])
        self.assertEqual(first["sim_time_s"], 2)
        self.assertEqual(first["events"], 9)

    def test_manifest_change_requires_new_provenance(self):
        self.manifest["seed"] += 1
        with self.assertRaisesRegex(ContractError, "checksum"):
            replay(self.manifest, self.log)

    def test_trainee_cannot_pause(self):
        self.log["events"][3]["producer"] = "trainee"
        with self.assertRaisesRegex(ContractError, "authority"):
            replay(self.manifest, self.log)

    def test_step_while_paused_is_rejected(self):
        self.log["events"][4].update(action="step", producer="scripted-source", payload={"dt_s": 1})
        with self.assertRaisesRegex(ContractError, "pause freezes"):
            replay(self.manifest, self.log)

    def test_out_of_order_and_duplicate_events(self):
        for field, value, message in [("sequence", 3, "Sequence"), ("event_id", "e-1", "duplicate")]:
            with self.subTest(field=field):
                log = copy.deepcopy(self.log)
                log["events"][1][field] = value
                with self.assertRaisesRegex(ContractError, message):
                    replay(self.manifest, log)

    def test_timestamp_drift(self):
        self.log["events"][5]["sim_time_s"] = 2
        with self.assertRaisesRegex(ContractError, "timestamp"):
            replay(self.manifest, self.log)

    def test_missing_final_event(self):
        self.log["events"].pop()
        with self.assertRaisesRegex(ContractError, "Incomplete"):
            replay(self.manifest, self.log)

    def test_unknown_cue(self):
        self.log["events"][4]["payload"]["cue"] = "unsupported"
        with self.assertRaisesRegex(ContractError, "cue"):
            replay(self.manifest, self.log)

    def test_acknowledgement_requires_injected_cue(self):
        self.log["events"][6]["payload"]["cue"] = "never-injected"
        with self.assertRaisesRegex(ContractError, "acknowledgement"):
            replay(self.manifest, self.log)

    def test_changed_expected_result_is_rejected(self):
        self.log["expected_summary"]["sim_time_s"] = 999
        with self.assertRaisesRegex(ContractError, "debrief"):
            replay(self.manifest, self.log)

    def test_reset_clears_cues_and_starts_new_episode(self):
        # Reset after the paused injection; stop in the new episode without acknowledgement.
        events = copy.deepcopy(self.log["events"][:5])
        events += [
            dict(event_id="reset", sequence=6, episode=0, sim_time_s=1,
                 producer="instructor", action="reset", payload={}),
            dict(event_id="restart", sequence=7, episode=1, sim_time_s=0,
                 producer="instructor", action="start", payload={}),
            dict(event_id="end", sequence=8, episode=1, sim_time_s=0,
                 producer="instructor", action="stop", payload={})]
        self.manifest["expected_actions"] = [e["action"] for e in events]
        states = [("ready",0,0,[]), ("running",0,0,[]), ("running",1,0,[]),
                  ("paused",1,0,[]), ("paused",1,0,["navigation-display-unavailable"]),
                  ("ready",0,1,[]), ("running",0,1,[]), ("stopped",0,1,[])]
        trace = [dict(sequence=i,state=s,sim_time_s=t,episode=p,active_cues=a,acknowledged_cues=[])
                 for i,(s,t,p,a) in enumerate(states,1)]
        expected = dict(scenario_id=self.manifest["scenario_id"],revision="1",events=8,
                        episode=1,state="stopped",sim_time_s=0,acknowledged_cues=[],
                        objective_met=False,trace_sha256=digest(trace))
        log = dict(manifest_sha256=digest(self.manifest), events=events, expected_summary=expected)
        self.assertFalse(replay(self.manifest, log)["objective_met"])
        log["events"][6]["episode"] = 0
        with self.assertRaisesRegex(ContractError, "episode"):
            replay(self.manifest, log)

    def test_reset_while_running_is_rejected(self):
        self.log["events"][2].update(action="reset", producer="instructor", payload={})
        with self.assertRaisesRegex(ContractError, "Reset"):
            replay(self.manifest, self.log)

    def test_unknown_action_and_wrong_frame(self):
        self.log["events"][0]["action"] = "arbitrary"
        with self.assertRaisesRegex(ContractError, "Unknown"):
            replay(self.manifest, self.log)
        self.manifest["frame"] = "NED"
        with self.assertRaisesRegex(ContractError, "frame"):
            replay(self.manifest, self.log)


if __name__ == "__main__":
    unittest.main()
