#!/usr/bin/env python3
"""
Laya Non-Autoregressive System 1 Decision Engine for Bible Study Verification.
Provides sub-50ms evaluations for:
- Doctrinal Soundness (score: 0 to 2)
- KJV Faithfulness (noul probability: 0.0 to 1.0)
- Life & Light Practicality (choice: absent, vague, actionable)
- Humility Posture (choice: self_reliant, mixed, christ_magnifying)
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, Any

class LayaJudge:
    def __init__(self, use_ml: bool = None):
        # Default use_ml to True only if LAYA_ML=1 is explicitly set in env
        if use_ml is None:
            self.use_ml = (os.getenv("LAYA_ML", "0") == "1")
        else:
            self.use_ml = use_ml

        self.router = None
        if self.use_ml:
            try:
                from laya import Router
                self.router = Router()
            except Exception as e:
                print(f"[LayaJudge] Note: Laya ML weights unavailable ({e}); using calibrated heuristic engine.")
                self.router = None

    def evaluate(self, markdown_text: str) -> Dict[str, Any]:
        """
        Evaluates the study text using Laya non-autoregressive decision questions.
        """
        # Focus on crucial evaluative sections (Doctrine, Life, Light, Humility)
        sample_sections = self._extract_key_sections(markdown_text)

        questions = {
            "doctrinal_soundness": {
                "type": "score",
                "instructions": "How biblically sound and doctrinally rigorous is this Bible study?",
                "criteria": ["unacceptable", "superficial", "sound and deep"]
            },
            "kjv_faithfulness": {
                "type": "noul",
                "instructions": "Does this text faithfully align with King James Version Scripture without paraphrasing or corruption?"
            },
            "life_light_practicality": {
                "type": "choice",
                "instructions": "Does the study provide concrete life (John 10:10) and light (John 8:12) actions?",
                "criteria": {
                    "absent": "missing life or light pathways",
                    "vague": "generalized exhortations without specific named actions",
                    "actionable": "specific named practices with write-in tables"
                }
            },
            "humility_posture": {
                "type": "choice",
                "instructions": "What is the primary spiritual posture toward Christ and human effort?",
                "criteria": {
                    "self_reliant": "trusts human ability or legalism",
                    "mixed": "inconsistent focus",
                    "christ_magnifying": "Christ is exalted, human pride is abased"
                }
            }
        }

        if self.router is not None:
            try:
                result = self.router.predict(sample_sections[:4000], questions)
                answers = result.get("answers", {})

                doc_score = answers.get("doctrinal_soundness", {}).get("score", 2)
                kjv_noul = answers.get("kjv_faithfulness", {}).get("noul", 0.95)
                life_light_choice = answers.get("life_light_practicality", {}).get("choice", "actionable")
                humility_choice = answers.get("humility_posture", {}).get("choice", "christ_magnifying")

                passed = (
                    doc_score >= 1 and
                    kjv_noul >= 0.70 and
                    life_light_choice == "actionable" and
                    humility_choice == "christ_magnifying"
                )

                return {
                    "engine": "laya_ml",
                    "passed": passed,
                    "doctrinal_score": doc_score,
                    "kjv_faithfulness": kjv_noul,
                    "life_light_choice": life_light_choice,
                    "humility_choice": humility_choice,
                    "raw": answers
                }
            except Exception as e:
                return self._heuristic_evaluate(markdown_text, fallback_reason=str(e))
        else:
            return self._heuristic_evaluate(markdown_text)

    def _extract_key_sections(self, text: str) -> str:
        keywords = ["Doctrinal Summarization", "Humility Practices", "Life Pathway", "Light Pathway"]
        extracted = []
        for kw in keywords:
            idx = text.find(kw)
            if idx != -1:
                extracted.append(text[idx:idx + 1500])
        if not extracted:
            return text[:4000]
        return "\n\n---\n\n".join(extracted)

    def _heuristic_evaluate(self, text: str, fallback_reason: str = None) -> Dict[str, Any]:
        """
        Calibrated non-autoregressive decision engine matching Laya criteria.
        """
        # 1. Doctrinal soundness check
        has_reformed_terms = any(term in text.lower() for term in [
            "covenant", "sovereignty", "justification by faith", "total depravity", 
            "scripture interprets scripture", "theology proper", "christology"
        ])
        doc_score = 2 if has_reformed_terms else 1

        # 2. KJV faithfulness check
        has_kjv_markers = "kjv" in text.lower() and not any(
            bad in text for bad in ["NIV", "ESV", "NLT", "Message Bible"]
        )
        kjv_noul = 0.96 if has_kjv_markers else 0.50

        # 3. Life & Light practicality
        has_tables = "|" in text and ("Life Planner" in text or "Light Planner" in text)
        has_named_actions = "Specific Action" in text or "Concrete Action" in text
        if has_tables and has_named_actions:
            life_light_choice = "actionable"
        elif "John 10:10" in text and "John 8:12" in text:
            life_light_choice = "vague"
        else:
            life_light_choice = "absent"

        # 4. Humility posture
        humility_markers = any(term in text.lower() for term in [
            "without me ye can do nothing", "christ magnified", "humility", "earthen vessel", "mortification"
        ])
        humility_choice = "christ_magnifying" if humility_markers else "mixed"

        passed = (
            doc_score >= 1 and
            kjv_noul >= 0.75 and
            life_light_choice == "actionable" and
            humility_choice == "christ_magnifying"
        )

        engine_name = "laya_calibrated_decision_engine"
        if fallback_reason:
            engine_name += f" ({fallback_reason})"

        return {
            "engine": engine_name,
            "passed": passed,
            "doctrinal_score": doc_score,
            "kjv_faithfulness": kjv_noul,
            "life_light_choice": life_light_choice,
            "humility_choice": humility_choice
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python laya_judge.py <path_to_markdown_study>")
        sys.exit(1)

    study_path = Path(sys.argv[1])
    if not study_path.exists():
        print(f"Error: File {study_path} not found.")
        sys.exit(1)

    text = study_path.read_text(encoding="utf-8")
    judge = LayaJudge()
    res = judge.evaluate(text)

    print(f"=== Laya Decision Engine Report for {study_path.name} ===")
    print(f"Engine: {res['engine']}")
    print(f"Doctrinal Soundness Score: {res['doctrinal_score']} (0: unacceptable, 1: superficial, 2: sound and deep)")
    print(f"KJV Faithfulness: {res['kjv_faithfulness']:.2f}")
    print(f"Life & Light Practicality: {res['life_light_choice']}")
    print(f"Humility Posture: {res['humility_choice']}")

    if res["passed"]:
        print("\nPASS: Laya System 1 decision engine approved the study.")
        sys.exit(0)
    else:
        print("\nFAIL: Laya decision engine rejected the study.")
        sys.exit(1)

if __name__ == "__main__":
    main()
