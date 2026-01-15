#!/usr/bin/env python3
"""
Quick check: try to instantiate sd.Sofascore for several leagues.
Adjust candidate names if needed.
"""
import traceback
import soccerdata as sd

print("soccerdata version:", getattr(sd, "__version__", "unknown"))
print("sd.Sofascore docstring (short):\n", (sd.Sofascore.__doc__ or "").strip()[:400], "\n---\n")

leagues_candidates = {
    "Bundesliga": ["Bundesliga", "GER-Bundesliga", "Germany-Bundesliga"],
    "LaLiga": ["LaLiga", "ESP-La Liga", "ESP-LaLiga", "La Liga"],
    "Serie A": ["Serie A", "ITA-Serie A", "Italy-Serie A"],
    "Premier League": ["Premier League", "ENG-Premier League", "England-Premier League"],
}

seasons = "2022/2023"

results = {}

for nice_name, candidates in leagues_candidates.items():
    results[nice_name] = {"success": False, "used": None, "errors": []}
    for cand in candidates:
        try:
            print(f"Trying {nice_name} with candidate '{cand}' ...", end=" ")
            # Try with a single string first
            obj = sd.Sofascore(leagues=cand, seasons=seasons)
            # If instantiation succeeded, record and break
            print("OK")
            results[nice_name]["success"] = True
            results[nice_name]["used"] = cand
            results[nice_name]["object_repr"] = repr(obj)
            # If the object provides a minimal method that triggers load, you can try to call it here,
            # but that may perform network IO. We're only testing instantiation.
            break
        except Exception as e:
            print("FAILED")
            results[nice_name]["errors"].append({"candidate": cand, "error": str(e)})
            # continue to next candidate
    # As a fallback: try passing a list of candidates
    if not results[nice_name]["success"]:
        try:
            print(f"Trying {nice_name} with candidate list {candidates} ...", end=" ")
            obj = sd.Sofascore(leagues=candidates, seasons=seasons)
            print("OK (list)")
            results[nice_name]["success"] = True
            results[nice_name]["used"] = f"list:{candidates}"
            results[nice_name]["object_repr"] = repr(obj)
        except Exception as e:
            print("FAILED (list)")
            results[nice_name]["errors"].append({"candidate": "list", "error": str(e)})

print("\nSummary:")
for league, info in results.items():
    if info["success"]:
        print(f" - {league}: OK (used: {info['used']})")
    else:
        print(f" - {league}: FAILED")
        for err in info["errors"]:
            print(f"    tried {err['candidate']}: {err['error']}")