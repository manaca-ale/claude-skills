# Visual Content Classification Schema v2.0

## Purpose

Reference taxonomy for automated media asset indexing. Standardized codes mapped
to Stash tags for scene marker creation. This file is user-editable.

## Positional Configuration (P-codes)

| Code | Common Name                  | Stash Tag                       | Stash ID | Visual Descriptor                                        |
|------|------------------------------|---------------------------------|----------|----------------------------------------------------------|
| P01  | Missionary                   | Missionary                      | 109      | Subject A supine, subject B superior, face-to-face       |
| P02  | Doggy Style                  | Doggy Style                     | 55       | Subject A prone/kneeling, subject B posterior approach    |
| P03  | Cowgirl                      | Cowgirl                         | 105      | Subject A superior/seated, facing subject B              |
| P04  | Reverse Cowgirl              | Reverse Cowgirl                 | 124      | Subject A superior, facing away from subject B           |
| P05  | Spooning                     | Spooning                        | 139      | Both subjects lateral, same orientation                  |
| P06  | 69                           | 69                              | 157      | Subjects inverted, head-to-pelvis bilateral              |
| P07  | Prone Bone                   | Prone Bone                      | 116      | Subject A prone flat, subject B on top, posterior         |
| P08  | Standing Sex                 | Standing Sex                    | 209      | Both subjects standing/vertical                          |
| P09  | Standing Doggy               | Standing Doggy Style            | 12       | Subject A bent forward standing, subject B posterior      |
| P10  | Piledriver                   | Piledriver                      | 450      | Subject A inverted/folded, subject B above               |
| P11  | Full Nelson                  | Full Nelson                     | 523      | Subject A held from behind, arms locked                  |
| P12  | Riding                       | Riding                          | 117      | Subject A on top, bouncing motion                        |
| P13  | Scissoring                   | Scissoring                      | 485      | Subjects interlocked at legs                             |
| P14  | Facesitting                  | Facesitting                     | 125      | Subject A seated on face of subject B                    |
| P15  | Legs Up Missionary           | Legs Up Missionary              | 235      | Missionary with legs elevated                            |
| P16  | Back Shot                    | Back Shot                       | 236      | Rear approach, close-up posterior                         |
| P17  | Aerial Cowgirl               | Aerial Cowgirl                  | 479      | Subject A suspended, cowgirl without support             |
| P18  | Squatting Cowgirl            | Squatting Cowgirl               | 129      | Subject A squatting on top, facing subject B             |
| P19  | Side Cowgirl                 | Side Cowgirl                    | 365      | Cowgirl from lateral angle                               |
| P20  | Lazy Reverse Cowgirl         | Lazy Reverse Cowgirl            | 130      | Reverse cowgirl, reclined/relaxed position               |
| P21  | Squatting Reverse Cowgirl    | Squatting Reverse Cowgirl       | 151      | Squatting on top, facing away                            |
| P22  | Standing 69                  | Standing 69                     | 284      | 69 position while standing                               |
| P23  | Lotus                        | Riding                          | 117      | Seated face-to-face, legs wrapped                        |
| P24  | Butterfly                    | Standing Sex                    | 209      | Supine at edge, partner standing                         |
| P00  | Indeterminate                | —                               | —        | Position not classifiable from frame                     |

> **Note:** P12 (Riding) and P23 (Lotus) both map to Stash tag "Riding" (ID 117).
> Lotus is a variant of riding. They produce identical markers in Stash but remain
> distinct codes for classification granularity.

## Interaction Modality (M-codes)

| Code | Common Name                  | Stash Tag                       | Stash ID | Descriptor                                               |
|------|------------------------------|---------------------------------|----------|----------------------------------------------------------|
| M01  | Vaginal Sex                  | Vaginal Sex                     | 56       | Vaginal penetrative contact                              |
| M02  | Anal Sex                     | Anal Sex                        | 280      | Anal penetrative contact                                 |
| M03  | Blowjob                      | Blowjob                         | 17       | Oral-penile stimulation                                  |
| M04  | Deepthroat                   | Deepthroat                      | 88       | Deep oral-penile stimulation                             |
| M05  | Handjob                      | Handjob                         | 101      | Manual penile stimulation                                |
| M06  | Cunnilingus                  | Oral Sex                        | 76       | Oral-vulvar stimulation                                  |
| M07  | Rimming                      | Rimming                         | 191      | Oral-anal stimulation                                    |
| M08  | Fingering                    | Fingering                       | 473      | Digital penetration/stimulation                          |
| M09  | Titjob                       | Titjob                          | 287      | Mammary stimulation of penis                             |
| M10  | Footjob                      | Footjob                         | 548      | Pedal stimulation                                        |
| M11  | Masturbation                 | Masturbation                    | 102      | Self-stimulation (solo or mutual)                        |
| M12  | Kissing                      | Kissing                         | 108      | Non-genital intimate oral contact                        |
| M13  | Tease                        | Tease                           | 168      | Teasing, provocative non-contact                         |
| M14  | Striptease                   | Striptease                      | 377      | Undressing/disrobing                                     |
| M15  | Double Blowjob               | Double Blowjob                  | 73       | Two mouths, oral-penile stimulation                      |
| M16  | Sloppy Blowjob               | Sloppy Blowjob                  | 500      | Exaggerated saliva oral-penile                           |
| M17  | Creampie                     | Creampie                        | 110      | Internal ejaculation visible                             |
| M18  | Cumshot                      | Cumshot                         | 86       | External ejaculation                                     |
| M19  | Double Penetration           | Double Penetration (DP)         | 275      | Simultaneous dual penetration                            |
| M20  | Facesitting                  | Facesitting                     | 125      | Oral stimulation via seated position                     |
| M00  | Indeterminate                | —                               | —        | Modality not classifiable from frame                     |

## Subject Count (S-codes)

| Code | Common Name | Stash Tag    | Stash ID |
|------|-------------|--------------|----------|
| S0   | None        | —            | —        |
| S1   | Solo        | Solo         | 549      |
| S2   | Duo         | —            | —        |
| S3   | Threesome   | Threesome    | 43       |

> **Note:** S2 (Duo) has no Stash tag because it is the default case for most
> classified content. Only Solo (S1) and Threesome (S3) are tagged.

## POV Variants (optional secondary tag — NOT used in P##-M##-S# classification)

When scene is filmed in POV perspective, add as secondary Stash tag:

| POV Variant             | Stash Tag                      | Stash ID |
|-------------------------|--------------------------------|----------|
| Missionary POV          | Missionary - POV               | 179      |
| Doggy Style POV         | Doggy Style - POV              | 228      |
| Cowgirl POV             | Cowgirl - POV                  | 221      |
| Reverse Cowgirl POV     | Reverse Cowgirl - POV          | 237      |
| Blowjob POV             | Blowjob - POV                 | 167      |
| Standing Blowjob        | Standing Blowjob               | 203      |

## Anal Position Variants (optional secondary tag — NOT used in P##-M##-S# classification)

| Variant                        | Stash Tag                      | Stash ID |
|--------------------------------|--------------------------------|----------|
| Anal Doggy Style               | Anal Doggy Style               | 574      |
| Anal Standing Doggy Style      | Anal Standing Doggy Style      | 579      |
| Anal Reverse Cowgirl           | Anal Reverse Cowgirl - POV     | 573      |

## Classification Output Format

Each frame receives: `P##-M##-S#`

Claude outputs ONLY codes during classification (anti-block).
The `resolve_labels.py` script converts codes → Common Names and generates Stash markers.

## How to Edit

- To add a new position: add a row with next P-code (P25, P26...)
- To add a new modality: add a row with next M-code (M21, M22...)
- The **Stash Tag** and **Stash ID** columns enable automatic marker creation
- If a Stash tag doesn't exist yet, create it first via the Stash UI, then add the ID here
