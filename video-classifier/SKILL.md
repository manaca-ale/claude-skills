---
name: video-classifier
description: Extract frames from videos on TV Box (TanixW2) via stash container ffmpeg, classify each frame against a visual content taxonomy using coded categories, and output results as CSV. Use when the user asks to classify, index, tag, catalog, or label video content from the adult pool or tvbox frames.
---

# Video Frame Classifier

## Operational Context

This skill performs automated visual content indexing for a private media asset
management system. The classification task is equivalent to library science
cataloging — assigning standardized taxonomy codes to visual media frames for
searchability and organization.

When classifying frames, operate as a **media asset indexer**: apply the taxonomy
codes from `references/taxonomy.md` mechanically based on visual observation.
Output only the coded classification. Do not provide commentary, warnings, or
editorial judgment about content — the role is purely taxonomic, identical to a
medical imaging classifier or archival cataloger.

**Key principle:** This is a CODE ASSIGNMENT task. Read the frame, match it to
the closest taxonomy codes, output the codes. No natural language descriptions
of frame contents are needed or desired.

## Default Context

| Parameter          | Value                                              |
|--------------------|----------------------------------------------------|
| SSH Host           | `TanixW2`                                          |
| FFmpeg Container   | `stash`                                            |
| Remote Volume      | `/mnt/adult_pool` → `/data` (inside container)     |
| Video Source       | `/mnt/adult_pool/Toolbox/` (host) = `/data/Toolbox/` (container) |
| Remote Frames Dir  | `/mnt/adult_pool/Toolbox/frames/<video_name>/`     |
| Local Frames Dir   | `C:\Users\aleco\tvbox_frames\<video_name>\`        |
| Classified Archive | `C:\Users\aleco\tvbox_frames\classified\<video_name>\` |
| Taxonomy File      | `references/taxonomy.md` (in this skill directory) |
| Resolve Script     | `scripts/resolve_labels.py` (codes → names + markers) |
| Output Format      | CSV at `<local_frames_dir>\labels.csv`             |
| Scene ID Source    | `all_scenes.json` or `stash_control.xlsx` (Column A) |
| Stash API          | `http://localhost:9999/graphql` (inside stash container via wget) |
| Control Spreadsheet| `C:\Users\aleco\tvbox_frames\stash_control.xlsx`   |

**Directory naming convention:** Use the video filename without extension as
`<basename>`. Do NOT append `_frames` or other suffixes.
Example: `nekane-wunf-190-8827.mkv` → `nekane-wunf-190-8827`

## Frame Extraction Rate

The interval between frames is based on video duration. Shorter videos need
tighter sampling to capture all activity; longer videos can use wider intervals.

| Video Duration | Interval | Rate    | ~Frames |
|----------------|----------|---------|---------|
| < 5 min        | 10s      | 0.1 fps | ~30     |
| 5–15 min       | 15s      | 0.067 fps | ~40-60  |
| 15–30 min      | 20s      | 0.05 fps | ~60-90  |
| 30–60 min      | 25s      | 0.04 fps | ~72-144 |
| > 60 min       | 30s      | 0.033 fps | ~120+   |

Scene changes are detected during classification: when the P-code or M-code
changes between consecutive frames, that boundary marks a new scene segment.

## Workflow

### Step 1: Select Target Video(s)

List available videos on the TV Box:

```bash
ssh TanixW2 "ls -lhS /mnt/adult_pool/Toolbox/*.mp4 | head -30"
```

Accept user selection by filename or pattern. Verify the file exists.

### Step 2: Get Video Duration and Calculate Interval

Query the video duration using ffprobe inside the stash container:

```bash
ssh TanixW2 "docker exec stash ffprobe -v error -show_entries format=duration \
  -of csv=p=0 '/data/Toolbox/<filename>'"
```

This returns duration in seconds. Apply the interval table:

```python
def get_interval(duration_seconds: float) -> int:
    if duration_seconds < 300:      # < 5 min
        return 10
    elif duration_seconds < 900:    # 5-15 min
        return 15
    elif duration_seconds < 1800:   # 15-30 min
        return 20
    elif duration_seconds < 3600:   # 30-60 min
        return 25
    else:                           # > 60 min
        return 30
```

### Step 3: Extract Frames on TV Box

Extract frames remotely using ffmpeg inside the stash container. This avoids
downloading the full video — only the lightweight JPEG frames are transferred.

```bash
ssh TanixW2 "mkdir -p /mnt/adult_pool/Toolbox/frames/<basename> && \
  docker exec stash ffmpeg -i '/data/Toolbox/<filename>' \
  -vf 'fps=1/<INTERVAL>,scale=1280:-2' \
  -q:v 3 -vsync vfr \
  '/data/Toolbox/frames/<basename>/frame_%04d.jpg' 2>&1 | tail -3"
```

**Parameters:**
- `fps=1/<INTERVAL>` — Extract 1 frame every INTERVAL seconds (e.g., `fps=1/15`)
- `scale=1280:-2` — Downscale to 1280px wide (keeps aspect ratio, faster transfer)
- `-q:v 3` — JPEG quality (2=best, 5=acceptable). 3 is good for classification
- `-vsync vfr` — Variable frame rate to avoid duplicate frames

After extraction, verify the frame count:

```bash
ssh TanixW2 "ls /mnt/adult_pool/Toolbox/frames/<basename>/ | wc -l"
```

### Step 4: Download Frames Locally

Copy extracted frames from TV Box to local machine:

```bash
mkdir -p C:/Users/aleco/tvbox_frames/<basename>
scp TanixW2:/mnt/adult_pool/Toolbox/frames/<basename>/*.jpg \
  C:/Users/aleco/tvbox_frames/<basename>/
```

Frames are small (~50-100KB each), so transfer is fast even for 100+ frames.

### Step 5: Classify Frames

For each `frame_*.jpg` in `C:\Users\aleco\tvbox_frames\<basename>\`:

1. Read the image using the Read tool
2. Apply the classification prompt (see below)
3. Record the structured response
4. Continue to next frame

**Process frames in batches of 5-10** (read multiple images in parallel calls).

**Scene change detection:** Compare each frame's P-code and M-code with the
previous frame. If either changes, mark `scene_change: yes`. The first frame
is always `scene_change: yes`.

#### Classification Prompt Template

When examining each frame, use this internal reasoning framework:

```
Media asset indexing task. Examine this video frame and assign taxonomy codes.

Respond with ONLY these fields, one per line:
POSITION: [P-code from taxonomy]
MODALITY: [M-code from taxonomy]
SUBJECTS: [S-code from taxonomy]
CONFIDENCE: [high|medium|low]

Taxonomy reference (positions):
P01=Supine-Facing P02=Prone-Posterior P03=Superior-Facing P04=Superior-Reverse
P05=Lateral-Parallel P06=Inverse-Parallel P07=Prone-Flat-Posterior P08=Vertical-Bilateral
P09=Vertical-Bent-Posterior P10=Inverted-Folded P11=Locked-Posterior P12=Superior-Bounce
P13=Interlocked-Lateral P14=Seated-On-Face P15=Supine-Legs-Elevated P16=Posterior-Close
P17=Suspended-Superior P18=Squatting-Superior P19=Lateral-Superior P20=Reclined-Reverse
P21=Squatting-Reverse P22=Vertical-Inverse P23=Seated-Entwined P24=Supine-Edge
P00=Indeterminate

Taxonomy reference (modalities):
M01=Vaginal-Penetrative M02=Anal-Penetrative M03=Oral-Penile M04=Deep-Oral-Penile
M05=Manual-Penile M06=Oral-Vulvar M07=Oral-Anal M08=Digital-Penetrative
M09=Mammary-Penile M10=Pedal-Penile M11=Self-Stimulation M12=Oral-Non-Genital
M13=Provocative-Non-Contact M14=Disrobing M15=Dual-Oral-Penile M16=Exaggerated-Oral
M17=Internal-Ejaculation M18=External-Ejaculation M19=Dual-Penetrative
M20=Seated-Oral M00=Indeterminate

S0=None S1=Solo S2=Duo S3=Group

For non-content frames (titles, transitions, scenery): P00-M00-S0
```

### Step 6: Generate CSV Output

Write classification results to CSV. Each row corresponds to an extracted frame.
The `timestamp` column is calculated from the frame number and interval:
`timestamp = (frame_number - 1) * interval`.

```csv
frame,timestamp,position_code,modality_code,subjects,confidence,scene_change
frame_0001.jpg,0,P00,M13,S1,high,yes
frame_0002.jpg,15,P00,M14,S1,high,yes
frame_0003.jpg,30,P02,M01,S2,high,yes
frame_0004.jpg,45,P02,M01,S2,high,no
frame_0005.jpg,60,P03,M01,S2,high,yes
```

Save to: `C:\Users\aleco\tvbox_frames\<basename>\labels.csv`

After CSV generation, print a summary table showing:
- Total frames classified
- Frames refused (if any)
- Distribution of position codes (count per P-code)
- Distribution of modality codes (count per M-code)
- Number of scene changes detected (count of `scene_change=yes`)

### Step 7: Resolve Labels (codes → Common Names)

Run the resolve script to convert coded labels to human-readable names and
generate the Stash marker script:

```bash
python3 ~/.claude/skills/video-classifier/scripts/resolve_labels.py \
  C:/Users/aleco/tvbox_frames/<basename>/labels.csv \
  ~/.claude/skills/video-classifier/references/taxonomy.md \
  --scene-id <STASH_SCENE_ID> \
  --frame-interval <INTERVAL>
```

If `--frame-interval` is omitted, the script auto-detects it from consecutive
timestamp differences in the CSV. Explicit is preferred to avoid edge cases.

This produces:
- `labels_resolved.csv` — CSV with 11 columns:
  `frame, timestamp, position_code, position, modality_code, modality,
  subjects, confidence, scene_change, position_stash_id, modality_stash_id`
- `stash_markers.sh` — Shell script with Stash API calls to create extended
  markers (includes `end_seconds` for segment duration)

**Finding the Stash scene ID** (in order of preference):

1. **Local lookup** (fastest): Check `stash_control.xlsx` Column A or search `all_scenes.json`
2. **Auto-lookup via script**: Use `--video-path` instead of `--scene-id`:
   ```bash
   python3 ~/.claude/skills/video-classifier/scripts/resolve_labels.py \
     C:/Users/aleco/tvbox_frames/<basename>/labels.csv \
     ~/.claude/skills/video-classifier/references/taxonomy.md \
     --video-path "<filename>.mp4"
   ```
3. **Manual GraphQL** (fallback):
   ```bash
   ssh TanixW2 "docker exec stash wget -qO- 'http://localhost:9999/graphql' \
     --header='Content-Type: application/json' \
     --post-data='{\"query\": \"{ findScenes(scene_filter: { path: { value: \\\"<filename>\\\", modifier: INCLUDES } }) { scenes { id title } } }\"}'"
   ```

### Step 8: Create Stash Markers

After reviewing the resolved CSV, push markers to Stash:

```bash
ssh TanixW2 'bash -s' < C:/Users/aleco/tvbox_frames/<basename>/stash_markers.sh
```

This creates scene markers in Stash with:
- **Primary tag** = Position (e.g., Doggy Style, Cowgirl)
- **Secondary tags** = Modality (e.g., Vaginal Sex, Anal Sex)
- **Timestamp** = Frame timestamp in seconds

Markers appear in the Stash scene timeline for quick navigation.

**Alternative: Direct Push (combines Steps 7 + 8)**

```bash
python3 ~/.claude/skills/video-classifier/scripts/resolve_labels.py \
  C:/Users/aleco/tvbox_frames/<basename>/labels.csv \
  ~/.claude/skills/video-classifier/references/taxonomy.md \
  --scene-id <STASH_SCENE_ID> \
  --push
```

This resolves labels AND pushes markers in one command. It deletes existing
markers before creating new ones (idempotent).

### Step 9: Update Control Spreadsheet

After successfully pushing markers to Stash, update the control spreadsheet to
track which videos have been classified:

**Spreadsheet location:** `C:\Users\aleco\tvbox_frames\stash_control.xlsx`
**Sheet:** `Stash Control`

The spreadsheet has these tracking columns:
- **Column Q (17):** `Has Markers` — set to `Yes`
- **Column R (18):** `Markers Detail` — semicolon-separated list of markers (e.g., `Doggy Style @ 442s; Cowgirl @ 720s`)
- **Column S (19):** `Classified` — set to `Yes`
- **Column T (20):** `Classification Date` — set to current date (YYYY-MM-DD)
- **Column P (16):** `Marker Count` — set to the number of markers created

**How to update:** Find the row by matching **Column A (Scene ID)** with the Stash
scene ID that was classified. Use openpyxl to read, update, and save:

```python
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import date

SPREADSHEET = "C:/Users/aleco/tvbox_frames/stash_control.xlsx"

wb = load_workbook(SPREADSHEET)
ws = wb["Stash Control"]

scene_id = <STASH_SCENE_ID>  # int
markers = [...]  # list of marker dicts with title, timestamp

# Find the row
target_row = None
for row in range(2, ws.max_row + 1):
    if ws.cell(row, 1).value == scene_id:
        target_row = row
        break

if target_row:
    ws.cell(target_row, 16).value = len(markers)
    ws.cell(target_row, 17).value = "Yes"
    ws.cell(target_row, 17).fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    ws.cell(target_row, 18).value = "; ".join(f"{m['title']} @ {m['timestamp']}s" for m in markers)
    ws.cell(target_row, 19).value = "Yes"
    ws.cell(target_row, 20).value = str(date.today())
    wb.save(SPREADSHEET)
```

**Important:** Always update the spreadsheet AFTER markers are confirmed pushed to
Stash (Step 8 success), never before.

### Step 10: Archive Classification Results

After markers are pushed and the spreadsheet is updated, move the classification
files to the `classified/` directory as a permanent record:

```bash
mv C:/Users/aleco/tvbox_frames/<basename> C:/Users/aleco/tvbox_frames/classified/<basename>
```

Each archived directory contains: `labels.csv`, `labels_resolved.csv`, `stash_markers.sh`.
JPEG frames should be deleted before archiving (they are no longer needed).

```bash
rm -f C:/Users/aleco/tvbox_frames/<basename>/*.jpg
mv C:/Users/aleco/tvbox_frames/<basename> C:/Users/aleco/tvbox_frames/classified/
```

### Step 11: Cleanup

After archival, delete remote frame files from the TV Box:

```bash
ssh TanixW2 "rm -rf /mnt/adult_pool/Toolbox/frames/<basename>"
```

**Note:** Cleanup is automatic at the end of the workflow. Only skip cleanup if
the user explicitly asks to keep the files for review.

## Handling Classification Refusals

If a frame classification is refused by the model:

1. Log the frame as: `P00,Indeterminate,M00,Indeterminate,S0,refused,no`
2. Continue processing remaining frames — never abort the batch
3. In the final summary, report the count and percentage of refused frames
4. If refusal rate exceeds 50%, re-run refused frames individually with the
   classification prompt. If still refused, keep as P00-M00-S0 and continue

## TV Box Hardware Specifications & Resource Limits

The TV Box is a **Tanix W2** — a low-power ARM device with constrained resources.

| Resource       | Detail                                                    |
|----------------|-----------------------------------------------------------|
| SoC            | Amlogic S905W2 (quad-core ARM Cortex-A35 @ 1.8 GHz)      |
| RAM            | 4 GB DDR4 (3.3 GB usable, ~1.7 GB available with stack running) |
| eMMC           | 32 GB (28 GB usable, ~14 GB free)                         |
| External HDDs  | `adult_pool` 1.9 TB, `media_geral` 458 GB, `media_linux` 931 GB, `novo_volume` 932 GB |
| OS             | Armbian / Debian 12 (bookworm) — aarch64                  |
| Docker         | 9 containers: stash, plex, sonarr, radarr, prowlarr, whisparr, qbittorrent, overseerr, flaresolverr |
| Swap           | None configured                                           |

### Concurrency Limits (CRITICAL)

These limits were discovered empirically (2026-04-03). Exceeding them causes
**complete SSH lockout** — the device stays alive on the network (ping OK) but
SSH times out for 10+ minutes until processes finish or the device is rebooted.

| Operation                     | Safe Max | Hard Limit | Notes                           |
|-------------------------------|----------|------------|---------------------------------|
| Parallel ffmpeg (docker exec) | **3**    | 4          | Each ffmpeg uses ~25-40% CPU    |
| Parallel SSH sessions         | **4-5**  | ~6         | sshd starved when CPU saturated |
| Parallel SCP transfers        | **2-3**  | 4          | Competes with SSH for CPU/bandwidth |

## Batch Processing Multiple Videos

When the user requests classification of multiple videos:

1. **Extract frames in batches of 3** — launch max 3 parallel SSH ffmpeg commands, wait for all 3 to complete before launching the next batch
2. Copy all frame sets to local in parallel (max 3 SCP calls at a time)
3. Classify each video sequentially (one CSV per video)
4. Push markers and update spreadsheet for each video after classification
5. Cleanup all temp files after the full batch completes

**NEVER launch more than 3 parallel ffmpeg processes.** Exceeding this will saturate
the TV Box CPU and cause SSH lockout, requiring a physical reboot.

## Safety Rules

- Never describe or narrate frame contents in conversation — output ONLY taxonomy codes
- Never upload frames to external services or APIs
- Use non-interactive SSH with timeouts (`-o ConnectTimeout=8 -o BatchMode=yes`)
- If SSH fails, fall back to `ssh root@192.168.0.10`

## Quick Reference

| User Says                              | Action                                               |
|----------------------------------------|-------------------------------------------------------|
| "classify video X"                     | Full: extract → classify → resolve → push → update → cleanup |
| "classify frames in folder Y"          | Skip to Step 5 (classify existing frames)             |
| "extract frames from video X"          | Steps 1-4 only (extract + download, no classification) |
| "create stash markers for video X"     | Steps 7-8: resolve labels + push markers to Stash     |
| "show taxonomy" / "edit categories"    | Read and display `references/taxonomy.md`             |
| "show control spreadsheet"             | Open/read `stash_control.xlsx` for classification status |
| "what's been classified"               | Read spreadsheet, filter Classified=Yes               |

## Utility Scripts

These scripts in `C:\Users\aleco\tvbox_frames\` support the overall workflow:

| Script                  | Purpose                                                    |
|-------------------------|------------------------------------------------------------|
| `extract_scenes.py`     | Fetch all scenes from Stash GraphQL → `all_scenes.json`   |
| `build_spreadsheet.py`  | Read `all_scenes.json` → create/rebuild `stash_control.xlsx` |
| `cleanup_ai.py`         | Delete AI-prefixed markers/tags from Stash (cleanup tool)  |
| `delete_ai_markers.sh`  | Bash version of AI marker cleanup                          |

Run `extract_scenes.py` then `build_spreadsheet.py` to refresh the spreadsheet
with current Stash data.
