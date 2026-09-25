#!/usr/bin/env python3
"""
Structural Conformance Checker for KJV Bible Studies.
Verifies that all 19 components of the KJV 7.2 + 8.2 synthesized template,
the 7 Berean Council seats, the 5-level question ladder, the 9 doctrinal heads,
the Humility/Life/Light practices, write-in planners, and theological guards are present.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Any

REQUIRED_COMPONENTS = [
    (1, "Header & Passage Citation", [r"Header", r"Passage Citation", r"Chapter"]),
    (2, "The Hook / Opening Scenario", [r"Hook", r"Opening Scenario", r"Dilemma"]),
    (3, "Historical & Philological Context", [r"Historical", r"Philological", r"Context"]),
    (4, "Literary Structure & Hinge Words", [r"Literary Structure", r"Hinge Words"]),
    (5, "Verbatim KJV Passage Text", [r"Verbatim KJV", r"Passage Text", r"Scripture Text"]),
    (6, "Level 1: Observation Questions", [r"Level 1", r"Observation"]),
    (7, "Level 2: Interpretation Questions", [r"Level 2", r"Interpretation"]),
    (8, "Level 3: Application Questions", [r"Level 3", r"Application"]),
    (9, "Level 4: Christocentric & Humility Questions", [r"Level 4", r"Christocentric", r"Humility"]),
    (10, "Level 5: Life & Light Questions", [r"Level 5", r"Life & Light", r"Bring It"]),
    (11, "Berean Council Consensus Briefs", [r"Berean Council", r"Consensus Briefs"]),
    (12, "Church History & Confessional Witness", [r"Church History", r"Confessional Witness", r"Creeds"]),
    (13, "Systematic Doctrinal Summarization", [r"Doctrinal Summarization", r"Systematic Doctrines", r"Doctrines"]),
    (14, "Three Humility Practices", [r"Humility Practices", r"Three.*Humility"]),
    (15, "The Life Pathway (John 10:10)", [r"Life Pathway", r"John 10:10"]),
    (16, "The Life Planner", [r"Life Planner"]),
    (17, "The Light Pathway (John 8:12)", [r"Light Pathway", r"John 8:12"]),
    (18, "The Light Planner", [r"Light Planner"]),
    (19, "Closing Prayer, Benediction & Leader's Answer Key", [r"Prayer", r"Leader.*Answer Key", r"Teacher.*Guide"]),
]

COUNCIL_SEATS = [
    "Philologist",
    "Historian",
    "Literary Scholar",
    "Theologian",
    "Church Historian",
    "Pastor",
    "Educator"
]

DOCTRINAL_HEADS = [
    ("Theology Proper", [r"Theology Proper", r"Doctrine of God"]),
    ("Christology", [r"Christology", r"Person.*Work of Christ"]),
    ("Pneumatology", [r"Pneumatology", r"Holy Spirit"]),
    ("Anthropology", [r"Anthropology", r"Nature of Man", r"Image of God"]),
    ("Hamartiology", [r"Hamartiology", r"Doctrine of Sin", r"Total Depravity"]),
    ("Soteriology", [r"Soteriology", r"Salvation", r"Justification", r"Grace"]),
    ("Ecclesiology", [r"Ecclesiology", r"The Church", r"Body of Christ"]),
    ("Eschatology", [r"Eschatology", r"Last Things", r"Resurrection", r"Judgment"]),
    ("Sanctification", [r"Sanctification", r"Christian Living", r"Holy Living", r"Holiness"])
]

GUARDS = [
    ("Abundance Guard", [r"Abundance Guard", r"more abundantly.*not material prosperity", r"prosperity gospel"]),
    ("Love Guard", [r"Love Guard", r"glare.*not light", r"without love is glare"])
]

class StructureChecker:
    def __init__(self, min_word_count: int = 1500):
        self.min_word_count = min_word_count

    def check(self, markdown_text: str) -> Dict[str, Any]:
        words = markdown_text.split()
        word_count = len(words)

        missing_components = []
        found_components = []

        for point_num, name, patterns in REQUIRED_COMPONENTS:
            matched = False
            for pat in patterns:
                if re.search(pat, markdown_text, re.IGNORECASE):
                    matched = True
                    break
            if matched:
                found_components.append((point_num, name))
            else:
                missing_components.append((point_num, name))

        missing_seats = []
        for seat in COUNCIL_SEATS:
            if not re.search(r'\b' + re.escape(seat) + r'\b', markdown_text, re.IGNORECASE):
                missing_seats.append(seat)

        found_doctrines = []
        missing_doctrines = []
        for d_name, patterns in DOCTRINAL_HEADS:
            matched = False
            for pat in patterns:
                if re.search(pat, markdown_text, re.IGNORECASE):
                    matched = True
                    break
            if matched:
                found_doctrines.append(d_name)
            else:
                missing_doctrines.append(d_name)

        missing_guards = []
        for g_name, patterns in GUARDS:
            matched = False
            for pat in patterns:
                if re.search(pat, markdown_text, re.IGNORECASE):
                    matched = True
                    break
            if not matched:
                missing_guards.append(g_name)

        passed = (
            len(missing_components) == 0 and
            len(missing_seats) == 0 and
            len(missing_doctrines) <= 2 and  # Allow up to 2 heads absent if passage is narrow, but require majority
            len(missing_guards) == 0 and
            word_count >= self.min_word_count
        )

        return {
            "passed": passed,
            "word_count": word_count,
            "min_word_count": self.min_word_count,
            "components_found": len(found_components),
            "components_total": len(REQUIRED_COMPONENTS),
            "missing_components": missing_components,
            "council_seats_found": len(COUNCIL_SEATS) - len(missing_seats),
            "missing_seats": missing_seats,
            "doctrines_found": len(found_doctrines),
            "missing_doctrines": missing_doctrines,
            "missing_guards": missing_guards
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python structure_checker.py <path_to_markdown_study>")
        sys.exit(1)

    study_path = Path(sys.argv[1])
    if not study_path.exists():
        print(f"Error: File {study_path} not found.")
        sys.exit(1)

    text = study_path.read_text(encoding="utf-8")
    checker = StructureChecker()
    res = checker.check(text)

    print(f"=== Structure Checker Report for {study_path.name} ===")
    print(f"Word Count: {res['word_count']} (Min required: {res['min_word_count']})")
    print(f"Template Points Found: {res['components_found']}/{res['components_total']}")
    print(f"Berean Council Seats Found: {res['council_seats_found']}/7")
    print(f"Doctrinal Heads Found: {res['doctrines_found']}/9")

    if res["missing_components"]:
        print("\nMissing Template Points:")
        for num, name in res["missing_components"]:
            print(f"  - Point {num}: {name}")

    if res["missing_seats"]:
        print(f"\nMissing Council Seats: {', '.join(res['missing_seats'])}")

    if res["missing_doctrines"]:
        print(f"\nMissing Doctrinal Heads: {', '.join(res['missing_doctrines'])}")

    if res["missing_guards"]:
        print(f"\nMissing Theological Guards: {', '.join(res['missing_guards'])}")

    if res["passed"]:
        print("\nPASS: Structural conformance verified across all required dimensions.")
        sys.exit(0)
    else:
        print("\nFAIL: Study failed structural conformance criteria.")
        sys.exit(1)

if __name__ == "__main__":
    main()
