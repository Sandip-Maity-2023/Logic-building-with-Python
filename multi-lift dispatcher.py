import json
from typing import List, Dict

# ---------------- Helper functions ---------------- #
def eta(lift, call_floor):
    """Rough ETA: distance in floors * 1s + door time (2s)."""
    return abs(lift["floor"] - call_floor) * 1 + 2

def direction(lift):
    return lift["dir"]

def penalty(lift, call_floor, call_dir):
    """Directional preference penalty."""
    dir_pen = 0
    if lift["dir"] == 0:  # idle
        return 0
    if (call_floor - lift["floor"]) * lift["dir"] < 0:
        dir_pen += 3  # reversal
    if lift["dir"] != call_dir:
        dir_pen += 5  # opposite call
    return dir_pen

# ---------------- Dispatcher logic ---------------- #
def assign_calls(F, lifts, calls):
    time = 0
    results = []
    waits = []

    for call in calls:
        t, floor, dirn = call["t"], call["floor"], call["dir"]
        time = max(time, t)

        best_lift, best_score, best_eta = None, float("inf"), None

        for lid, lift in lifts.items():
            e = eta(lift, floor)
            p = penalty(lift, floor, dirn)
            score = e + p
            if score < best_score:
                best_score, best_lift, best_eta = score, lid, e

        # Assign
        lifts[best_lift]["stops"].append(floor)
        lifts[best_lift]["floor"] = floor
        lifts[best_lift]["dir"] = dirn
        wait = best_eta
        waits.append(wait)
        results.append(f"t={t}, {floor}{dirn:+} -> {best_lift} (ETA={wait}s)")

    avg_wait = round(sum(waits)/len(waits), 2)
    max_wait = max(waits)
    total_travel = sum(waits)  # approximate total travel
    metrics = f"avg_wait={avg_wait}s, max_wait={max_wait}s, total_travel={total_travel} floors"

    return results, metrics

# ---------------- Main CLI ---------------- #
def main():
    print("=== Multi-Lift Dispatcher ===\n")

    # Read JSON input file
    path = input("Enter JSON file path (default: lifts.json): ").strip() or "lifts.json"
    with open(path, "r") as f:
        data = json.load(f)

    F = data["F"]
    lifts = {lid: info for lid, info in data["lifts"].items()}
    calls = data["calls"]

    results, metrics = assign_calls(F, lifts, calls)

    print("\n--- Assignments ---")
    for r in results:
        print(r)

    print("\n--- Metrics ---")
    print(metrics)

if __name__ == "__main__":
    main()
