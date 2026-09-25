#!/usr/bin/env python3
"""
Master Checker Orchestrator for KJV Bible Studies.
Executes all verification layers:
1. Deterministic Verse Checker (data/kjv.json exact matches)
2. Structural Conformance Checker (19 points, 7 council seats, 9 doctrines)
3. Laya System 1 Decision Engine (non-autoregressive classification)

Exits 0 if all checkers pass, or outputs actionable feedback and exits 1.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

from verse_checker import VerseChecker
from structure_checker import StructureChecker
from laya_judge import LayaJudge

class MasterChecker:
    def __init__(self):
        self.verse_checker = VerseChecker()
        self.structure_checker = StructureChecker(min_word_count=1200)
        self.laya_judge = LayaJudge()

    def verify_file(self, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {
                "passed": False,
                "error": f"File {file_path} not found"
            }

        text = file_path.read_text(encoding="utf-8")

        # Layer 1: Verse Check
        verse_res = self.verse_checker.check_text(text)

        # Layer 2: Structure Check
        struct_res = self.structure_checker.check(text)

        # Layer 3: Laya Check
        laya_res = self.laya_judge.evaluate(text)

        all_passed = (
            verse_res["passed"] and
            struct_res["passed"] and
            laya_res["passed"]
        )

        feedback_items = []
        if not verse_res["passed"]:
            feedback_items.append("SCRIPTURE QUOTE MISMATCHES DETECTED:")
            for m in verse_res["mismatches"]:
                feedback_items.append(f"  - {m['reference']}: expected '{m.get('expected')}', got '{m['actual']}'")

        if not struct_res["passed"]:
            feedback_items.append("STRUCTURAL DEFICIENCIES:")
            if struct_res["missing_components"]:
                for num, name in struct_res["missing_components"]:
                    feedback_items.append(f"  - Missing Section {num}: {name}")
            if struct_res["missing_seats"]:
                feedback_items.append(f"  - Missing Berean Council Seats: {', '.join(struct_res['missing_seats'])}")
            if struct_res["missing_doctrines"]:
                feedback_items.append(f"  - Missing Doctrinal Categories: {', '.join(struct_res['missing_doctrines'])}")
            if struct_res["missing_guards"]:
                feedback_items.append(f"  - Missing Guards: {', '.join(struct_res['missing_guards'])}")
            if struct_res["word_count"] < struct_res["min_word_count"]:
                feedback_items.append(f"  - Word count {struct_res['word_count']} is below minimum {struct_res['min_word_count']}")

        if not laya_res["passed"]:
            feedback_items.append("LAYA DECISION ENGINE REJECTIONS:")
            feedback_items.append(f"  - Doctrinal Score: {laya_res['doctrinal_score']} (must be >= 1)")
            feedback_items.append(f"  - KJV Faithfulness: {laya_res['kjv_faithfulness']} (must be >= 0.70)")
            feedback_items.append(f"  - Life/Light Practicality: {laya_res['life_light_choice']} (must be 'actionable')")
            feedback_items.append(f"  - Humility Posture: {laya_res['humility_choice']} (must be 'christ_magnifying')")

        return {
            "passed": all_passed,
            "verse_results": verse_res,
            "structure_results": struct_res,
            "laya_results": laya_res,
            "feedback": "\n".join(feedback_items) if feedback_items else "All verification layers passed."
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python master_checker.py <path_to_markdown_study>")
        sys.exit(1)

    path = Path(sys.argv[1])
    checker = MasterChecker()
    res = checker.verify_file(path)

    print(f"\n=======================================================")
    print(f"MASTER CHECKER REPORT: {path.name}")
    print(f"=======================================================")
    print(f"Verse Integrity:     {'PASS' if res['verse_results']['passed'] else 'FAIL'} ({res['verse_results']['exact_matches']}/{res['verse_results']['total_checked']} quotes match KJV)")
    print(f"Structure Integrity: {'PASS' if res['structure_results']['passed'] else 'FAIL'} ({res['structure_results']['components_found']}/19 components)")
    print(f"Laya Decision:       {'PASS' if res['laya_results']['passed'] else 'FAIL'} ({res['laya_results']['engine']})")
    print(f"OVERALL VERDICT:     {'PASS' if res['passed'] else 'FAIL'}")
    print(f"=======================================================")

    if not res["passed"]:
        print("\nACTIONABLE FEEDBACK FOR REVISION:")
        print(res["feedback"])
        sys.exit(1)
    else:
        print("\nSUCCESS: All criteria met without error.")
        sys.exit(0)

if __name__ == "__main__":
    main()
