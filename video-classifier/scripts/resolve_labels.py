#!/usr/bin/env python3
"""
resolve_labels.py — Converts coded labels CSV to human-readable CSV + Stash marker commands.

Usage:
    python resolve_labels.py labels.csv taxonomy.md [--scene-id SCENE_ID] [--output-dir DIR]

Inputs:
    labels.csv   — CSV with columns: frame,timestamp,position_code,modality_code,subjects,confidence,scene_change
    taxonomy.md  — Markdown taxonomy file with P-code/M-code tables containing Common Name and Stash ID

Outputs:
    labels_resolved.csv  — CSV with Common Names instead of codes
    stash_markers.sh     — Shell script with wget commands to create Stash scene markers
"""

import csv
import re
import sys
import os
import argparse
from pathlib import Path


def parse_taxonomy(taxonomy_path: str) -> dict:
    """Parse taxonomy.md and extract code -> (common_name, stash_tag, stash_id) mappings."""
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        content = f.read()

    mappings = {}
    # Match table rows: | CODE | Common Name | Stash Tag | Stash ID | ... |
    row_pattern = re.compile(
        r"\|\s*(P\d{2}|M\d{2}|S\d)\s*\|"   # Code
        r"\s*([^|]+?)\s*\|"                   # Common Name
        r"\s*([^|]*?)\s*\|"                   # Stash Tag
        r"\s*(\d+|—)\s*\|"                    # Stash ID
    )

    for match in row_pattern.finditer(content):
        code = match.group(1).strip()
        common_name = match.group(2).strip()
        stash_tag = match.group(3).strip()
        stash_id = match.group(4).strip()

        mappings[code] = {
            "common_name": common_name,
            "stash_tag": stash_tag if stash_tag != "—" else None,
            "stash_id": int(stash_id) if stash_id != "—" else None,
        }

    return mappings


def resolve_csv(input_csv: str, mappings: dict, output_csv: str):
    """Read coded CSV, resolve to Common Names, write resolved CSV."""
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    fieldnames = [
        "frame", "timestamp", "position_code", "position", "modality_code",
        "modality", "subjects", "confidence", "scene_change",
        "position_stash_id", "modality_stash_id",
    ]

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            p_code = row.get("position_code", "P00")
            m_code = row.get("modality_code", "M00")
            s_code = row.get("subjects", "S0")

            p_info = mappings.get(p_code, {"common_name": "Unknown", "stash_id": None})
            m_info = mappings.get(m_code, {"common_name": "Unknown", "stash_id": None})
            s_info = mappings.get(s_code, {"common_name": "Unknown", "stash_id": None})

            writer.writerow({
                "frame": row.get("frame", ""),
                "timestamp": row.get("timestamp", ""),
                "position_code": p_code,
                "position": p_info["common_name"],
                "modality_code": m_code,
                "modality": m_info["common_name"],
                "subjects": s_info["common_name"],
                "confidence": row.get("confidence", ""),
                "scene_change": row.get("scene_change", ""),
                "position_stash_id": p_info["stash_id"] or "",
                "modality_stash_id": m_info["stash_id"] or "",
            })

    print(f"[OK] Resolved CSV written to: {output_csv}")
    return rows, mappings


def generate_stash_markers(rows: list, mappings: dict, scene_id: str, output_sh: str,
                           frame_interval: int = 30):
    """Generate extended markers by grouping consecutive frames with same classification.

    Each marker covers the full duration of a position/act segment (start -> end).
    """
    if not scene_id:
        print("[SKIP] No --scene-id provided, skipping marker script generation.")
        return

    # Step 1: Group consecutive frames with same P+M code into segments
    segments = []
    current_segment = None

    for row in rows:
        p_code = row.get("position_code", "P00")
        m_code = row.get("modality_code", "M00")
        timestamp = int(row.get("timestamp", 0))

        # Skip non-content frames
        if p_code == "P00" and m_code == "M00":
            if current_segment:
                current_segment["end"] = timestamp
                segments.append(current_segment)
                current_segment = None
            continue

        # Determine primary tag
        p_info = mappings.get(p_code, {})
        m_info = mappings.get(m_code, {})

        if p_code != "P00" and p_info.get("stash_id"):
            primary_tag_id = p_info["stash_id"]
            primary_name = p_info.get("common_name", p_code)
            secondary_tag_ids = [m_info["stash_id"]] if m_info.get("stash_id") else []
            segment_key = f"{p_code}-{m_code}"
        elif m_code != "M00" and m_info.get("stash_id"):
            primary_tag_id = m_info["stash_id"]
            primary_name = m_info.get("common_name", m_code)
            secondary_tag_ids = []
            segment_key = f"P00-{m_code}"
        else:
            if current_segment:
                current_segment["end"] = timestamp
                segments.append(current_segment)
                current_segment = None
            continue

        # Same segment continues? Match on same primary tag (position or modality)
        if current_segment and current_segment["key"] == segment_key:
            current_segment["end"] = timestamp + frame_interval
        elif current_segment and current_segment["primary_tag_id"] == primary_tag_id:
            # Same primary tag but different secondary — extend the segment
            current_segment["end"] = timestamp + frame_interval
        else:
            # Close previous segment
            if current_segment:
                segments.append(current_segment)
            # Start new segment
            current_segment = {
                "key": segment_key,
                "start": timestamp,
                "end": timestamp + frame_interval,
                "title": primary_name,
                "primary_tag_id": primary_tag_id,
                "secondary_tag_ids": secondary_tag_ids,
            }

    # Close last segment
    if current_segment:
        segments.append(current_segment)

    # Step 2: Convert segments to markers
    markers = []
    for seg in segments:
        markers.append({
            "timestamp": seg["start"],
            "end_seconds": seg["end"],
            "title": seg["title"],
            "primary_tag_id": seg["primary_tag_id"],
            "secondary_tag_ids": seg["secondary_tag_ids"],
        })

    print(f"\n[SEGMENTS] Grouped {len(rows)} frames into {len(markers)} extended markers:", flush=True)
    for i, m in enumerate(markers, 1):
        start_m, start_s = divmod(m["timestamp"], 60)
        end_m, end_s = divmod(m["end_seconds"], 60)
        duration = m["end_seconds"] - m["timestamp"]
        print(f"  {i}. {m['title']:25s} {start_m:02d}:{start_s:02d} -> {end_m:02d}:{end_s:02d} ({duration}s)",
              flush=True)

    # Write shell script
    with open(output_sh, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/bash\n")
        f.write(f"# Stash scene markers for scene_id={scene_id}\n")
        f.write(f"# Generated by resolve_labels.py\n")
        f.write(f"# Total markers: {len(markers)}\n")
        f.write(f"#\n")
        f.write(f"# Run via: ssh TanixW2 'bash -s' < stash_markers.sh\n")
        f.write(f"# Or copy to TV Box and run locally.\n\n")
        f.write(f'STASH_URL="http://localhost:9999/graphql"\n\n')

        for i, m in enumerate(markers, 1):
            tag_ids = ", ".join(f'\\"{tid}\\"' for tid in m["secondary_tag_ids"])
            tag_array = f"[{tag_ids}]" if tag_ids else "[]"

            end_part = f', end_seconds: {m["end_seconds"]}' if m.get("end_seconds") else ""

            query = (
                f'mutation {{ sceneMarkerCreate(input: {{'
                f' scene_id: \\"{scene_id}\\",'
                f' title: \\"{m["title"]}\\",'
                f' seconds: {m["timestamp"]},'
                f' primary_tag_id: \\"{m["primary_tag_id"]}\\",'
                f' tag_ids: {tag_array}{end_part}'
                f' }}) {{ id title seconds end_seconds }} }}'
            )

            f.write(f"# Marker {i}: {m['title']} @ {m['timestamp']}s\n")
            f.write(
                f'docker exec stash wget -qO- "$STASH_URL" '
                f'--header="Content-Type: application/json" '
                f"--post-data='{{\"query\": \"{query}\"}}'\n"
            )
            f.write(f"echo \"  [{i}/{len(markers)}] {m['title']} @ {m['timestamp']}s\"\n\n")

    print(f"[OK] Stash marker script written to: {output_sh}")
    print(f"     {len(markers)} markers to create for scene_id={scene_id}")

    return markers


def print_summary(rows: list, mappings: dict):
    """Print distribution summary."""
    from collections import Counter

    positions = Counter()
    modalities = Counter()
    refused = 0

    for row in rows:
        p_code = row.get("position_code", "P00")
        m_code = row.get("modality_code", "M00")
        conf = row.get("confidence", "")

        if conf == "refused":
            refused += 1
            continue

        p_name = mappings.get(p_code, {}).get("common_name", p_code)
        m_name = mappings.get(m_code, {}).get("common_name", m_code)
        positions[p_name] += 1
        modalities[m_name] += 1

    print(f"\n{'='*50}")
    print(f"SUMMARY — {len(rows)} frames classified, {refused} refused")
    print(f"{'='*50}")

    print(f"\nPositions:")
    for name, count in positions.most_common():
        pct = count / len(rows) * 100
        print(f"  {name:30s} {count:4d} ({pct:5.1f}%)")

    print(f"\nModalities:")
    for name, count in modalities.most_common():
        pct = count / len(rows) * 100
        print(f"  {name:30s} {count:4d} ({pct:5.1f}%)")


def find_stash_scene_id(video_filename: str, ssh_host: str = "TanixW2") -> str | None:
    """Query Stash GraphQL API to find scene ID by video filename."""
    import subprocess
    import json
    import tempfile

    # Search by filename (not full path) for flexibility
    basename = os.path.basename(video_filename)

    # Write the GraphQL query to a temp script to avoid shell escaping hell
    graphql_query = json.dumps({
        "query": '{ findScenes(scene_filter: { path: { value: "'
                 + basename
                 + '", modifier: INCLUDES } }, filter: { per_page: 5 }) { scenes { id title files { path } } } }'
    })

    # Create a small script to run inside SSH — avoids nested quoting issues
    script = (
        f"docker exec stash wget -qO- 'http://localhost:9999/graphql' "
        f"--header='Content-Type: application/json' "
        f"--post-data='{graphql_query}'"
    )

    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", ssh_host, script],
            capture_output=True, text=True, timeout=15
        )

        # SSH banner goes to stderr, actual output to stdout
        output = result.stdout.strip()
        if not output:
            print(f"[ERROR] Empty response from Stash query")
            return None

        data = json.loads(output)
        scenes = data.get("data", {}).get("findScenes", {}).get("scenes", [])

        if not scenes:
            print(f"[WARN] No scene found in Stash for '{basename}'")
            return None

        if len(scenes) > 1:
            print(f"[WARN] Multiple scenes found for '{basename}', using first match:")
            for s in scenes:
                files = s.get("files", [])
                fpath = files[0]["path"] if files else "N/A"
                print(f"  id={s['id']} path={fpath}")

        scene_id = scenes[0]["id"]
        files = scenes[0].get("files", [])
        scene_path = files[0]["path"] if files else "N/A"
        print(f"[OK] Found Stash scene: id={scene_id} path={scene_path}")
        return scene_id

    except subprocess.TimeoutExpired:
        print("[ERROR] SSH timeout querying Stash")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[ERROR] Failed to parse Stash response: {e}")
        return None


def _ssh_graphql(query_json: str, ssh_host: str, timeout: int = 15):
    """Helper: run a GraphQL query on Stash via SSH+wget."""
    import subprocess
    cmd = (
        f"docker exec stash wget -qO- 'http://localhost:9999/graphql' "
        f"--header='Content-Type: application/json' "
        f"--post-data='{query_json}'"
    )
    result = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", ssh_host, cmd],
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout.strip()


def delete_existing_markers(scene_id: str, ssh_host: str = "TanixW2") -> int:
    """Delete all existing markers for a scene."""
    import json
    query = json.dumps({"query": f'{{ findScene(id: "{scene_id}") {{ scene_markers {{ id title seconds }} }} }}'})
    try:
        data = json.loads(_ssh_graphql(query, ssh_host))
        markers = data["data"]["findScene"]["scene_markers"]
    except Exception:
        print(f"[WARN] Could not fetch existing markers for scene {scene_id}")
        return 0

    if not markers:
        print(f"[OK] No existing markers to delete")
        return 0

    print(f"[DELETE] Removing {len(markers)} existing markers...", flush=True)
    for m in markers:
        try:
            _ssh_graphql(json.dumps({"query": f'mutation {{ sceneMarkerDestroy(id: "{m["id"]}") }}'}), ssh_host, 10)
        except Exception:
            pass
    print(f"[OK] Deleted {len(markers)} markers")
    return len(markers)


def push_markers_to_stash(markers: list, scene_id: str, ssh_host: str = "TanixW2",
                          delete_existing: bool = True) -> bool:
    """Push extended markers (with end_seconds) to Stash."""
    import json

    if delete_existing:
        delete_existing_markers(scene_id, ssh_host)

    print(f"\n[PUSH] Creating {len(markers)} extended markers for scene {scene_id}...", flush=True)
    success = 0
    failed = 0

    for i, m in enumerate(markers, 1):
        tag_ids_str = ", ".join(f'"{tid}"' for tid in m.get("secondary_tag_ids", []))
        tag_array = f"[{tag_ids_str}]" if tag_ids_str else "[]"
        end_part = f', end_seconds: {m["end_seconds"]}' if m.get("end_seconds") else ""

        graphql = json.dumps({"query": (
            f'mutation {{ sceneMarkerCreate(input: {{'
            f' scene_id: "{scene_id}", title: "{m["title"]}",'
            f' seconds: {m["timestamp"]}, primary_tag_id: "{m["primary_tag_id"]}",'
            f' tag_ids: {tag_array}{end_part}'
            f' }}) {{ id title seconds end_seconds }} }}'
        )})

        s_m, s_s = divmod(m["timestamp"], 60)
        e_m, e_s = divmod(m.get("end_seconds", 0), 60)
        dur = f"{s_m:02d}:{s_s:02d}->{e_m:02d}:{e_s:02d}"

        try:
            out = _ssh_graphql(graphql, ssh_host)
            if '"sceneMarkerCreate"' in out:
                print(f"  [{i}/{len(markers)}] {m['title']:25s} {dur} - OK")
                success += 1
            else:
                print(f"  [{i}/{len(markers)}] {m['title']:25s} {dur} - FAILED")
                failed += 1
        except Exception:
            print(f"  [{i}/{len(markers)}] {m['title']:25s} {dur} - TIMEOUT")
            failed += 1

    print(f"\n[DONE] {success} markers created, {failed} failed")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="Resolve coded labels to Common Names + Stash markers")
    parser.add_argument("labels_csv", help="Path to labels.csv (coded)")
    parser.add_argument("taxonomy_md", help="Path to taxonomy.md")
    parser.add_argument("--scene-id", help="Stash scene ID (if known)", default=None)
    parser.add_argument("--video-path", help="Video filename to auto-lookup scene ID in Stash", default=None)
    parser.add_argument("--push", action="store_true", help="Push markers to Stash immediately after generating")
    parser.add_argument("--frame-interval", type=int, default=None, help="Seconds between frames (auto-detected from CSV if omitted)")
    parser.add_argument("--ssh-host", help="SSH host alias (default: TanixW2)", default="TanixW2")
    parser.add_argument("--output-dir", help="Output directory (default: same as labels_csv)", default=None)
    args = parser.parse_args()

    output_dir = args.output_dir or str(Path(args.labels_csv).parent)

    resolved_csv = os.path.join(output_dir, "labels_resolved.csv")
    markers_sh = os.path.join(output_dir, "stash_markers.sh")

    # Parse taxonomy
    mappings = parse_taxonomy(args.taxonomy_md)
    print(f"[OK] Loaded {len(mappings)} taxonomy entries from {args.taxonomy_md}")

    # Resolve CSV
    rows, _ = resolve_csv(args.labels_csv, mappings, resolved_csv)

    # Auto-detect frame interval from CSV timestamps if not explicitly provided
    frame_interval = args.frame_interval
    if frame_interval is None:
        timestamps = sorted(int(r.get("timestamp", 0)) for r in rows if r.get("timestamp"))
        if len(timestamps) >= 2:
            diffs = [timestamps[i + 1] - timestamps[i] for i in range(min(len(timestamps) - 1, 20))]
            positive_diffs = [d for d in diffs if d > 0]
            if positive_diffs:
                frame_interval = min(positive_diffs)
                print(f"[AUTO] Detected frame interval: {frame_interval}s (from CSV timestamps)")
            else:
                frame_interval = 30
                print(f"[WARN] Could not detect interval, using default: {frame_interval}s")
        else:
            frame_interval = 30
            print(f"[WARN] Not enough timestamps to detect interval, using default: {frame_interval}s")

    # Determine scene ID
    scene_id = args.scene_id
    if not scene_id and args.video_path:
        scene_id = find_stash_scene_id(args.video_path, args.ssh_host)

    # Generate Stash markers (extended segments)
    markers = generate_stash_markers(rows, mappings, scene_id, markers_sh, frame_interval)

    # Print summary
    print_summary(rows, mappings)

    # Push to Stash if requested
    if args.push and scene_id and markers:
        push_markers_to_stash(markers, scene_id, args.ssh_host)
    elif args.push and not scene_id:
        print("\n[SKIP] Cannot push: no scene ID found. Use --scene-id or --video-path.")


if __name__ == "__main__":
    main()
