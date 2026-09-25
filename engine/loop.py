#!/usr/bin/env python3
"""
Autonomous Bible Study Loop Engine.
Implements the 6-stage Loop Engineering cycle:
  TRIGGER -> PLAN -> ACT -> OBSERVE -> VERIFY -> DECIDE

Enforces the 5 Stop Families:
- DONE: All checks green (Verse + Structure + Laya).
- CAP: Max retries per chapter (default 3), max runtime.
- STUCK: Identical failure 3 times in a row.
- DANGER: Tampering with protected files (data, prompts, verifiers).
- HUMAN: Sentinel file .loop-stop pauses loop gracefully.

Maintains progress/progress.json, progress/progress.md, and progress/loop-log.csv.
"""

import os
import sys
import time
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROG_DIR = BASE_DIR / "progress"
STUDIES_DIR = BASE_DIR / "studies"
SCRIPTS_DIR = BASE_DIR / "scripts"
VERIFIER_DIR = BASE_DIR / "verifier"
PROMPTS_DIR = BASE_DIR / "prompts"

# Add directories to path
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(VERIFIER_DIR))

from verifier.master_checker import MasterChecker
from engine.generator import ChapterGenerator

PROTECTED_PATHS = [
    DATA_DIR / "kjv.json",
    DATA_DIR / "books.json",
    PROMPTS_DIR / "kjv_master_prompt.md",
    PROMPTS_DIR / "rubric.md",
    VERIFIER_DIR / "verse_checker.py",
    VERIFIER_DIR / "structure_checker.py",
    VERIFIER_DIR / "laya_judge.py",
    VERIFIER_DIR / "master_checker.py",
]

class BibleStudyLoop:
    def __init__(self,
                 max_iters_per_chapter: int = 3,
                 stuck_limit: int = 3,
                 dry_run: bool = False,
                 halt_on_error: bool = False):
        self.max_iters = max_iters_per_chapter
        self.stuck_limit = stuck_limit
        self.dry_run = dry_run
        self.halt_on_error = halt_on_error

        self.progress_file = PROG_DIR / "progress.json"
        self.progress_md = PROG_DIR / "progress.md"
        self.log_file = PROG_DIR / "loop-log.csv"
        self.stop_file = BASE_DIR / ".loop-stop"
        self.escalations_file = PROG_DIR / "escalations.md"

        self.checker = MasterChecker()
        self.generator = ChapterGenerator()

        self._init_files()
        self.baseline_checksums = self._compute_checksums()

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _compute_checksums(self) -> Dict[str, str]:
        sums = {}
        for p in PROTECTED_PATHS:
            if p.exists():
                h = hashlib.sha256()
                h.update(p.read_bytes())
                sums[str(p)] = h.hexdigest()
        return sums

    def _check_danger(self) -> bool:
        current = self._compute_checksums()
        for p_str, original_hash in self.baseline_checksums.items():
            if current.get(p_str) != original_hash:
                return True
        return False

    def _init_files(self):
        PROG_DIR.mkdir(parents=True, exist_ok=True)
        STUDIES_DIR.mkdir(parents=True, exist_ok=True)

        if not self.log_file.exists():
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("iteration,started_at,chapter_ref,action,check_result,stop_reason,tokens_in,tokens_out,diff_lines,note\n")

    def log_row(self, iter_num: int, started_at: str, ref: str, action: str, check_result: str, stop_reason: str, diff_lines: int, note: str):
        clean_note = note.replace('"', "'").replace("\n", " ")[:120]
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f'{iter_num},"{started_at}","{ref}","{action}","{check_result}","{stop_reason}",,,{diff_lines},"{clean_note}"\n')

    def load_progress(self) -> Dict[str, Any]:
        with open(self.progress_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_progress(self, data: Dict[str, Any]):
        # Update summary counts
        completed = sum(1 for c in data["chapters"] if c["status"] == "completed")
        failed = sum(1 for c in data["chapters"] if c["status"] == "failed")
        pending = sum(1 for c in data["chapters"] if c["status"] == "pending")

        data["completed"] = completed
        data["failed"] = failed
        data["pending"] = pending

        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.update_progress_dashboard(data)

    def update_progress_dashboard(self, data: Dict[str, Any]):
        total = data["total_chapters"]
        comp = data["completed"]
        failed = data["failed"]
        pct = (comp / total * 100) if total else 0.0

        # Group by book
        by_book = {}
        for c in data["chapters"]:
            b_name = c["book_name"]
            by_book.setdefault(b_name, {"total": 0, "completed": 0, "failed": 0, "testament": c["testament"]})
            by_book[b_name]["total"] += 1
            if c["status"] == "completed":
                by_book[b_name]["completed"] += 1
            elif c["status"] == "failed":
                by_book[b_name]["failed"] += 1

        md = [
            "# Berean Council KJV Bible Study Loop Dashboard",
            f"**Last Updated:** {self._now()}",
            "",
            "## Overall Progress",
            f"- **Total Chapters:** {total}",
            f"- **Completed:** {comp} ({pct:.1f}%)",
            f"- **Failed / Escalated:** {failed}",
            f"- **Pending:** {data['pending']}",
            "",
            "## Progress by Book",
            "| Book | Testament | Chapters | Completed | Status |",
            "|---|---|---|---|---|"
        ]

        for b_name, stat in by_book.items():
            b_pct = (stat["completed"] / stat["total"] * 100) if stat["total"] else 0
            status_badge = "✅ Done" if stat["completed"] == stat["total"] else (f"🔄 {b_pct:.0f}%" if stat["completed"] > 0 else "⏳ Pending")
            if stat["failed"] > 0:
                status_badge += f" (⚠️ {stat['failed']} failed)"
            md.append(f"| {b_name} | {stat['testament']} | {stat['total']} | {stat['completed']} | {status_badge} |")

        with open(self.progress_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")

    def escalate(self, chapter: Dict[str, Any], reason: str, details: str):
        entry = [
            f"### Escalation: {chapter['book_name']} {chapter['chapter']} ({self._now()})",
            f"- **Reason:** {reason}",
            f"- **Iterations Tried:** {chapter['iterations']}",
            f"- **Details:**",
            "```text",
            details,
            "```",
            "---",
            ""
        ]
        with open(self.escalations_file, "a", encoding="utf-8") as f:
            f.write("\n".join(entry))
        print(f"[ESCALATION LOGGED] {chapter['book_name']} {chapter['chapter']} -> {reason}")

    def run_chapter(self, chapter: Dict[str, Any]) -> bool:
        ref = f"{chapter['book_name']} {chapter['chapter']}"
        out_path = BASE_DIR / chapter["output_path"]
        print(f"\n>>> [LOOP STAGE: PLAN] Target Chapter: {ref} (Output: {chapter['output_path']})")

        feedback = None
        last_failure_sig = ""
        same_failure_count = 0

        for attempt in range(1, self.max_iters + 1):
            started_at = self._now()
            print(f"--- Iteration {attempt}/{self.max_iters} for {ref} ---")

            # STOP FAMILY: HUMAN SENTINEL CHECK
            if self.stop_file.exists():
                print(f"[HUMAN STOP] Sentinel file {self.stop_file} detected. Pausing cleanly.")
                self.log_row(attempt, started_at, ref, "check_stop", "skipped", "HUMAN", 0, "Stop sentinel found")
                sys.exit(4)

            # STAGE: ACT (Generate / Re-draft)
            chapter["status"] = "in_progress"
            chapter["iterations"] = attempt
            chapter["last_run"] = started_at

            try:
                self.generator.generate(chapter, out_path, feedback=feedback, dry_run=self.dry_run)
            except Exception as e:
                print(f"[ACT ERROR] Generation failed: {e}")
                self.log_row(attempt, started_at, ref, "generate", "error", "ERROR", 0, str(e))
                feedback = f"Generation error: {e}"
                continue

            # STOP FAMILY: DANGER CHECK (Protected File Integrity)
            if self._check_danger():
                print("[DANGER] A protected system file was modified during generation! Halting immediately.")
                self.log_row(attempt, started_at, ref, "verify_safety", "fail", "DANGER", 0, "Protected file modified")
                sys.exit(5)

            # STAGE: VERIFY (Maker/Checker Separation: Verse + Structure + Laya)
            v_report = self.checker.verify_file(out_path)
            diff_lines = len(out_path.read_text(encoding="utf-8").splitlines()) if out_path.exists() else 0

            # STAGE: DECIDE
            if v_report["passed"]:
                # STOP FAMILY: DONE
                print(f"✅ DONE! All verifiers passed for {ref} on attempt {attempt}.")
                chapter["status"] = "completed"
                chapter["laya_score"] = v_report["laya_results"]["doctrinal_score"]
                chapter["verse_mismatches"] = 0
                self.log_row(attempt, started_at, ref, "master_verify", "PASS", "DONE", diff_lines, "All checks passed")
                return True

            # If failed, prepare feedback for next attempt
            feedback = v_report["feedback"]
            failure_sig = hashlib.md5(feedback.encode("utf-8")).hexdigest()

            # STOP FAMILY: STUCK (Identical error repeatedly)
            if failure_sig == last_failure_sig:
                same_failure_count += 1
            else:
                same_failure_count = 1
                last_failure_sig = failure_sig

            if same_failure_count >= self.stuck_limit:
                print(f"⛔ STUCK: Identical failure {same_failure_count} times in a row for {ref}.")
                chapter["status"] = "failed"
                self.log_row(attempt, started_at, ref, "master_verify", "FAIL", "STUCK", diff_lines, "Identical failure loop")
                self.escalate(chapter, "STUCK", feedback)
                return False

            print(f"❌ Attempt {attempt} failed verifications. Reason:\n{feedback[:250]}...")
            self.log_row(attempt, started_at, ref, "master_verify", "FAIL", "NOT_YET", diff_lines, feedback[:100])

        # STOP FAMILY: CAP REACHED
        print(f"⚠️ CAP: Maximum iterations ({self.max_iters}) reached for {ref}.")
        chapter["status"] = "failed"
        self.log_row(self.max_iters, started_at, ref, "master_verify", "FAIL", "CAP", diff_lines, "Max iterations reached")
        self.escalate(chapter, "CAP", feedback or "Max retries exceeded without pass")
        return False

    def run(self, filter_book: str = None, filter_chapter: int = None, filter_testament: str = None):
        data = self.load_progress()
        chapters = data["chapters"]

        # Filter chapters according to trigger
        targets = []
        for c in chapters:
            if filter_book and c["book_name"].lower() != filter_book.lower() and c.get("abbr", "").lower() != filter_book.lower():
                continue
            if filter_chapter is not None and c["chapter"] != filter_chapter:
                continue
            if filter_testament and c["testament"].upper() != filter_testament.upper():
                continue
            if c["status"] != "completed":
                targets.append(c)

        print(f"=== Berean Council Bible Study Loop Initiated ===")
        print(f"Target count to process: {len(targets)} chapters")
        print(f"Mode: {'DRY RUN (Safe mock)' if self.dry_run else 'REAL RUN'}")
        print(f"Max Iters/Chapter: {self.max_iters} | Stuck Limit: {self.stuck_limit}")
        print(f"Stop Sentinel Path: {self.stop_file}")

        success_count = 0
        fail_count = 0

        for i, ch_info in enumerate(targets, 1):
            print(f"\n=======================================================")
            print(f"Processing target [{i}/{len(targets)}]: {ch_info['book_name']} {ch_info['chapter']}")
            print(f"=======================================================")

            success = self.run_chapter(ch_info)
            if success:
                success_count += 1
            else:
                fail_count += 1
                if self.halt_on_error:
                    print("[HALT ON ERROR] Stopping loop due to chapter failure.")
                    break

            # Persist state after each chapter
            self.save_progress(data)

        print(f"\n=======================================================")
        print(f"Loop Run Complete. Processed: {len(targets)} | Success: {success_count} | Failed: {fail_count}")
        print(f"Dashboard updated at: {self.progress_md}")
        print(f"=======================================================")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="KJV Chapter Bible Study Loop Runner")
    parser.add_argument("--book", type=str, help="Process a specific book (e.g. 'Genesis' or 'Romans')")
    parser.add_argument("--chapter", type=int, help="Process a specific chapter number (requires --book)")
    parser.add_argument("--ref", type=str, help="Process a reference string e.g. 'Romans 8' or 'Genesis 1'")
    parser.add_argument("--testament", type=str, choices=["OT", "NT"], help="Process only OT or NT")
    parser.add_argument("--all", action="store_true", help="Process all pending chapters Genesis to Revelation")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run in safe mock dry-run mode")
    parser.add_argument("--max-iters", type=int, default=3, help="Max retry iterations per chapter")
    parser.add_argument("--halt-on-error", action="store_true", default=False, help="Halt loop on first failed chapter")

    args = parser.parse_args()

    # Parse --ref if provided
    book_arg = args.book
    chapter_arg = args.chapter
    if args.ref:
        parts = args.ref.strip().split()
        if len(parts) >= 2:
            book_arg = " ".join(parts[:-1])
            try:
                chapter_arg = int(parts[-1])
            except ValueError:
                book_arg = args.ref

    is_dry = args.dry_run or (os.getenv("DRY_RUN", "0") == "1")

    runner = BibleStudyLoop(
        max_iters_per_chapter=args.max_iters,
        dry_run=is_dry,
        halt_on_error=args.halt_on_error
    )

    runner.run(
        filter_book=book_arg,
        filter_chapter=chapter_arg,
        filter_testament=args.testament
    )

if __name__ == "__main__":
    main()
