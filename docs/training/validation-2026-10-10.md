# Instructor/Replay Contract Validation — 10 October 2026

## Tested scope

The `civil-navigation-interruption` revision-1 manifest and synthetic fixture
were checked offline using **Python 3.14.8** and the standard library. No simulator,
aircraft model, cloud service, network, cockpit or flight hardware was used.
Python 3.11+ is the source compatibility target; other versions were not run.

## Executed checks

| Check | Result |
| --- | --- |
| Replay command from the scenario guide | Passed; nine events, stopped at two seconds, objective acknowledged |
| `python -m unittest discover -s tests -v` | 13 tests passed |
| Golden trace | `abb83282ff05a12c46dfc95313164700d22b397b7cf74d2d36158bb28c5d02d8` |

The tests cover baseline reproducibility, changed manifest provenance, lifecycle
authority, paused stepping, duplicate/out-of-order events, timestamp drift,
missing terminal events, unknown/uninjected cues, debrief mismatch, reset cleanup,
stale episodes, reset while running, unsupported actions and frame rejection.

## Interpretation

The evidence supports the synthetic scenario/instructor/replay contract only.
It does not establish real-time behavior, authenticated instructor access,
aircraft dynamics accuracy, model qualification, simulator integration,
instructional effectiveness or certification. The script verifies a provided
log; it does not operate an interactive training session or generate flight data.

The organization profile moves this project from architecture (~20%) to
**contract harness (~30%)**. That editorial estimate recognizes this bounded
executable milestone while leaving a flight-simulation pilot, integration and
validated MVP pending. It is not a measured percentage of the full roadmap.

## Next acceptance gate

Select and pin one qualified civilian dynamics model; implement its local adapter;
record supported lifecycle/cue capabilities, units, frames and clock authority;
then replay actual model output within declared numerical tolerances. Unsupported
instructor actions must be rejected explicitly. Publish model-specific test
evidence before promoting the project to a flight-simulation pilot.

[Scenario guide](civil-navigation-interruption.md) · [Project overview](../../README.md)
