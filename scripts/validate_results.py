#!/usr/bin/env python3
"""
Lightweight automated validation script for experimental results in:
deepinverse-pnp-image-restoration

Validates step10_all_experiments.csv without external heavy dependencies.
Uses standard library csv, math, os, sys for maximum portability and compatibility.
"""
import os
import sys
import csv
import math
from collections import defaultdict


def validate_results():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    csv_path = os.path.join(repo_root, "results", "step10_all_experiments.csv")

    print("=================================================================")
    print(" DeepInverse PnP Restoration: Automated Results Validation")
    print("=================================================================")
    print(f"Checking data file: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"[-] ERROR: File not found: {csv_path}")
        return False

    required_columns = {"image", "repeat", "seed", "method", "psnr", "ssim", "runtime_sec"}
    expected_images = {"astronaut", "chelsea", "coffee", "rocket"}
    expected_methods = {"Direct DPIR", "Observation Init", "Coarse PnP Init"}
    expected_repeats = 5
    expected_total_rows = 60
    expected_observations = 20

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = set(reader.fieldnames or [])
        missing_cols = required_columns - header
        if missing_cols:
            print(f"[-] ERROR: Missing required CSV columns: {missing_cols}")
            return False

        rows = list(reader)

    print(f"[+] Loaded {len(rows)} records from CSV.")
    if len(rows) != expected_total_rows:
        print(f"[-] ERROR: Expected {expected_total_rows} rows, found {len(rows)}")
        return False

    # Structure and value validation
    observations = defaultdict(dict)
    seen_images = set()
    seen_methods = set()

    for idx, r in enumerate(rows, start=1):
        img = r["image"]
        method = r["method"]
        seen_images.add(img)
        seen_methods.add(method)

        # Validate categorical fields
        if img not in expected_images:
            print(f"[-] ERROR: Row {idx} has unrecognized image: '{img}'")
            return False
        if method not in expected_methods:
            print(f"[-] ERROR: Row {idx} has unrecognized method: '{method}'")
            return False

        # Validate numeric fields
        try:
            repeat = int(r["repeat"])
            seed = int(r["seed"])
            psnr = float(r["psnr"])
            ssim = float(r["ssim"])
            runtime = float(r["runtime_sec"])
        except ValueError as e:
            print(f"[-] ERROR: Row {idx} has non-numeric value: {e}")
            return False

        if not (1 <= repeat <= expected_repeats):
            print(f"[-] ERROR: Row {idx} repeat {repeat} out of range [1, {expected_repeats}]")
            return False
        if not (math.isfinite(psnr) and psnr > 0):
            print(f"[-] ERROR: Row {idx} invalid PSNR: {psnr}")
            return False
        if not (math.isfinite(ssim) and 0.0 <= ssim <= 1.0):
            print(f"[-] ERROR: Row {idx} invalid SSIM: {ssim}")
            return False
        if not (math.isfinite(runtime) and runtime > 0):
            print(f"[-] ERROR: Row {idx} invalid runtime: {runtime}")
            return False

        obs_key = (img, seed)
        if method in observations[obs_key]:
            print(f"[-] ERROR: Duplicate entry for observation {obs_key} and method '{method}'")
            return False

        observations[obs_key][method] = {
            "psnr": psnr,
            "ssim": ssim,
            "runtime": runtime,
            "repeat": repeat
        }

    print("[+] Column schema and data ranges verified successfully.")

    if seen_images != expected_images:
        print(f"[-] ERROR: Image set mismatch. Expected {expected_images}, found {seen_images}")
        return False
    if seen_methods != expected_methods:
        print(f"[-] ERROR: Method set mismatch. Expected {expected_methods}, found {seen_methods}")
        return False

    if len(observations) != expected_observations:
        print(f"[-] ERROR: Expected {expected_observations} distinct (image, seed) pairs, found {len(observations)}")
        return False

    for obs_key, methods_data in observations.items():
        if set(methods_data.keys()) != expected_methods:
            print(f"[-] ERROR: Incomplete method set for observation {obs_key}: {set(methods_data.keys())}")
            return False

    print(f"[+] Verified exactly {expected_observations} matched observations with 3 methods each.")

    # Statistical recalculation and check
    method_stats = {m: {"psnr": [], "ssim": [], "time": []} for m in expected_methods}
    for obs_key, mdata in observations.items():
        for m, vals in mdata.items():
            method_stats[m]["psnr"].append(vals["psnr"])
            method_stats[m]["ssim"].append(vals["ssim"])
            method_stats[m]["time"].append(vals["runtime"])

    def mean(v):
        return sum(v) / len(v)

    def std(v):
        m = mean(v)
        return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))

    # Expected benchmarks (within justified tolerance +/- 0.005)
    expected_aggregates = {
        "Direct DPIR": {"psnr": 28.4112, "ssim": 0.8588, "time": 0.2719},
        "Observation Init": {"psnr": 28.5295, "ssim": 0.8603, "time": 0.2735},
        "Coarse PnP Init": {"psnr": 28.5932, "ssim": 0.8622, "time": 0.3772},
    }

    print("\n--- Method-Level Aggregate Verification ---")
    for m in ["Direct DPIR", "Observation Init", "Coarse PnP Init"]:
        calc_psnr = mean(method_stats[m]["psnr"])
        calc_ssim = mean(method_stats[m]["ssim"])
        calc_time = mean(method_stats[m]["time"])
        exp = expected_aggregates[m]

        print(f"{m:18}: PSNR {calc_psnr:.4f} dB (exp ~{exp['psnr']:.4f}), "
              f"SSIM {calc_ssim:.4f} (exp ~{exp['ssim']:.4f}), "
              f"Time {calc_time:.4f} s (exp ~{exp['time']:.4f})")

        if abs(calc_psnr - exp["psnr"]) > 0.005:
            print(f"[-] ERROR: PSNR discrepancy for {m}: {calc_psnr} vs {exp['psnr']}")
            return False
        if abs(calc_ssim - exp["ssim"]) > 0.005:
            print(f"[-] ERROR: SSIM discrepancy for {m}: {calc_ssim} vs {exp['ssim']}")
            return False
        if abs(calc_time - exp["time"]) > 0.01:
            print(f"[-] ERROR: Runtime discrepancy for {m}: {calc_time} vs {exp['time']}")
            return False

    print("[+] Method-level averages match documented aggregates.")

    # Paired delta verification
    coarse_vs_direct = []
    obs_vs_direct = []
    coarse_vs_obs = []

    for obs_key, mdata in observations.items():
        p_direct = mdata["Direct DPIR"]["psnr"]
        p_obs = mdata["Observation Init"]["psnr"]
        p_coarse = mdata["Coarse PnP Init"]["psnr"]

        coarse_vs_direct.append(p_coarse - p_direct)
        obs_vs_direct.append(p_obs - p_direct)
        coarse_vs_obs.append(p_coarse - p_obs)

    mean_cd = mean(coarse_vs_direct)
    mean_od = mean(obs_vs_direct)
    mean_co = mean(coarse_vs_obs)

    pos_cd = sum(x > 0 for x in coarse_vs_direct)
    pos_od = sum(x > 0 for x in obs_vs_direct)
    pos_co = sum(x > 0 for x in coarse_vs_obs)

    print("\n--- Paired Difference Verification (N = 20 pairs) ---")
    print(f"Coarse PnP vs. Direct DPIR   : Mean {mean_cd:+.4f} dB (exp +0.1820 dB), "
          f"Positive: {pos_cd}/20 (100.0%)")
    print(f"Obs Init vs. Direct DPIR     : Mean {mean_od:+.4f} dB (exp +0.1183 dB), "
          f"Positive: {pos_od}/20 (90.0%) [Note: 2 negative trials on chelsea/rocket]")
    print(f"Coarse PnP vs. Obs Init      : Mean {mean_co:+.4f} dB (exp +0.0637 dB), "
          f"Positive: {pos_co}/20 (100.0%)")

    if abs(mean_cd - 0.1820) > 0.002 or pos_cd != 20:
        print(f"[-] ERROR: Coarse vs Direct delta validation failed: {mean_cd}, pos={pos_cd}")
        return False
    if abs(mean_od - 0.1183) > 0.002 or pos_od != 18:
        print(f"[-] ERROR: Obs vs Direct delta validation failed: {mean_od}, pos={pos_od}")
        return False
    if abs(mean_co - 0.0637) > 0.002 or pos_co != 20:
        print(f"[-] ERROR: Coarse vs Obs delta validation failed: {mean_co}, pos={pos_co}")
        return False

    print("[+] All paired difference statistics and trial win-rates validated successfully.")

    # Compute overhead
    direct_time = mean(method_stats["Direct DPIR"]["time"])
    coarse_time = mean(method_stats["Coarse PnP Init"]["time"])
    overhead = (coarse_time - direct_time) / direct_time * 100
    print(f"\n[+] Compute Overhead: {overhead:.1f}% additional runtime (exp ~38.7%)")
    if abs(overhead - 38.7) > 1.5:
        print(f"[-] ERROR: Runtime overhead mismatch: {overhead:.2f}%")
        return False

    print("\n=================================================================")
    print(" [PASSED] ALL RESULTS AND METHODOLOGICAL CHECKS VERIFIED!")
    print("=================================================================")
    return True


if __name__ == "__main__":
    success = validate_results()
    sys.exit(0 if success else 1)
