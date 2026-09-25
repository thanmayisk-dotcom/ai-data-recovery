# AI Data Recovery

An AI-assisted data recovery prototype designed to identify, reconstruct, analyze, and prioritize recoverable digital information from damaged or fragmented data.

## 🎯 Problem

Traditional file recovery can focus mainly on retrieving raw data. Our system goes further by analyzing recovered fragments, testing possible reconstructions, evaluating file integrity, and prioritizing the strongest recovery candidates.

## 💡 Our Approach

The system follows a recovery intelligence pipeline:

1. **Storage Scanning** — detects available files and identifies their types.
2. **File Classification** — recognizes supported formats such as JPEG, PNG, PDF, and TXT.
3. **Fragment Reconstruction** — combines available fragments to generate recovery candidates.
4. **Fragment Relationship Analysis** — evaluates possible fragment orders using file-structure evidence.
5. **Integrity Analysis** — checks whether reconstructed files are structurally valid.
6. **Recovery Intelligence** — assigns an evidence-based recovery score.
7. **Prioritization** — ranks recovery candidates according to their available evidence.
8. **Visual Intelligence** — compares recovered images using basic visual features.
9. **Recovery Preview** — displays the recovered file for verification.

## 🧠 Recovery Intelligence

Instead of simply reporting that a file was found, the system explains **why a recovery candidate was prioritized**.

For example, a JPEG candidate can receive evidence from:

- JPEG header detection
- JPEG end-marker detection
- Successful image verification
- Sufficient recovered data
- Fragment order supported by relationship analysis

The recovery score represents **evidence and integrity signals**, not a statistical probability of successful recovery.

## 🔄 Demonstrated Recovery

The prototype includes a controlled fragmented JPEG recovery scenario.

The system:

```text
Damaged / Fragmented Data
        ↓
File Detection
        ↓
Fragment Analysis
        ↓
Candidate Reconstruction
        ↓
Relationship Evaluation
        ↓
Integrity Verification
        ↓
Recovery Scoring
        ↓
Candidate Prioritization
        ↓
Recovered File Preview

