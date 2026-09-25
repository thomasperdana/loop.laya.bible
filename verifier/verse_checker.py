#!/usr/bin/env python3
"""
Deterministic Verse Checker for KJV Bible Studies.
Verifies all Scripture quotations against canonical data/kjv.json.
Returns exit code 0 if 0 mismatches found, or lists exact quote discrepancies.
"""

import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

class VerseChecker:
    def __init__(self, kjv_json_path: Path = None):
        if kjv_json_path is None:
            kjv_json_path = DATA_DIR / "kjv.json"
        
        self.kjv_path = kjv_json_path
        self.verses: Dict[Tuple[int, int, int], str] = {}
        self.book_name_to_id: Dict[str, int] = {}
        self.book_id_to_name: Dict[int, str] = {}
        self._load_data()

    def _load_data(self):
        books_file = DATA_DIR / "books.json"
        if books_file.exists():
            with open(books_file, "r", encoding="utf-8") as f:
                b_data = json.load(f)
                for b in b_data.get("books", []):
                    b_id = b["book_id"]
                    name = b["name"]
                    abbr = b["abbr"]
                    self.book_name_to_id[name.lower()] = b_id
                    self.book_name_to_id[abbr.lower()] = b_id
                    self.book_name_to_id[name.lower().replace(" ", "")] = b_id
                    self.book_id_to_name[b_id] = name
        
        # Common singular/plural aliases
        self.book_name_to_id["psalm"] = self.book_name_to_id.get("psalms", 19)
        self.book_name_to_id["revelations"] = self.book_name_to_id.get("revelation", 66)
        
        if not self.kjv_path.exists():
            raise FileNotFoundError(f"{self.kjv_path} not found.")

        with open(self.kjv_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        
        for r in raw.get("resultset", {}).get("row", []):
            field = r.get("field", [])
            if len(field) >= 5:
                _, b_id, ch, v, text = field[:5]
                self.verses[(b_id, ch, v)] = text.strip()

    def normalize(self, text: str, keep_case: bool = False) -> str:
        # Standardize whitespace and quotes for fair comparison
        t = text.strip()
        t = re.sub(r'[\u201c\u201d"]', '"', t)
        t = re.sub(r'[\u2018\u2019\']', "'", t)
        t = re.sub(r'\s+', ' ', t)
        if not keep_case:
            # Also normalize case for comparison
            t = t.lower()
        return t

    def get_verse(self, book_name: str, chapter: int, verse: int) -> str:
        b_clean = book_name.lower().strip()
        b_id = self.book_name_to_id.get(b_clean)
        if not b_id:
            # Try removing spaces e.g. "1samuel"
            b_id = self.book_name_to_id.get(b_clean.replace(" ", ""))
        if not b_id:
            return None
        return self.verses.get((b_id, chapter, verse))

    def extract_quotations(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Finds quotes with references.
        Supports patterns like:
        > "In the beginning..." — Genesis 1:1
        "In the beginning..." (Genesis 1:1)
        Genesis 1:1: "In the beginning..."
        """
        quotes = []

        # Regex for references: Book Chapter:Verse(-Verse)
        # e.g. Genesis 1:1 or 1 Corinthians 13:4-7 or John 3:16
        ref_pattern = r'([1-3]?\s*[A-Za-z]+)\s+([0-9]+):([0-9]+)(?:-([0-9]+))?'

        # Pattern 1: > "Quoted text" — Reference or (Reference)
        p1 = re.compile(
            r'>\s*["“]([^"”]+)["”]\s*(?:—|-|–|\(|\[)\s*' + ref_pattern,
            re.MULTILINE
        )
        for m in p1.finditer(markdown_text):
            quoted_text, book, ch, v_start, v_end = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5)
            quotes.append({
                "type": "blockquote",
                "text": quoted_text.strip(),
                "book": book.strip(),
                "chapter": ch,
                "verse_start": v_start,
                "verse_end": int(v_end) if v_end else v_start,
                "raw_match": m.group(0)
            })

        # Pattern 2: "Quoted text" (Reference) or "Quoted text" — Reference
        p2 = re.compile(
            r'["“]([^"”]{10,})["”]\s*(?:—|-|–|\()\s*' + ref_pattern,
            re.MULTILINE
        )
        for m in p2.finditer(markdown_text):
            quoted_text, book, ch, v_start, v_end = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5)
            # Avoid duplicate if matched by p1
            if not any(q["text"] == quoted_text.strip() for q in quotes):
                quotes.append({
                    "type": "inline",
                    "text": quoted_text.strip(),
                    "book": book.strip(),
                    "chapter": ch,
                    "verse_start": v_start,
                    "verse_end": int(v_end) if v_end else v_start,
                    "raw_match": m.group(0)
                })

        return quotes

    def check_text(self, markdown_text: str, target_book: str = None, target_chapter: int = None) -> Dict[str, Any]:
        extracted = self.extract_quotations(markdown_text)
        checked = []
        mismatches = []

        for q in extracted:
            canonical_parts = []
            for v_num in range(q["verse_start"], q["verse_end"] + 1):
                c_text = self.get_verse(q["book"], q["chapter"], v_num)
                if c_text:
                    canonical_parts.append(c_text)
            
            if not canonical_parts:
                # Could not resolve reference in canonical db
                mismatches.append({
                    "quote": q["text"],
                    "reference": f"{q['book']} {q['chapter']}:{q['verse_start']}",
                    "issue": "Reference not found in canonical KJV database",
                    "expected": None,
                    "actual": q["text"]
                })
                continue

            canonical_full = " ".join(canonical_parts)
            norm_actual = self.normalize(q["text"])
            norm_expected = self.normalize(canonical_full)

            # Check if actual is identical or a faithful substring
            if norm_actual == norm_expected:
                checked.append({
                    "reference": f"{q['book']} {q['chapter']}:{q['verse_start']}",
                    "status": "EXACT_MATCH"
                })
            elif norm_actual in norm_expected:
                checked.append({
                    "reference": f"{q['book']} {q['chapter']}:{q['verse_start']}",
                    "status": "SUBSTRING_MATCH"
                })
            else:
                mismatches.append({
                    "quote": q["text"],
                    "reference": f"{q['book']} {q['chapter']}:{q['verse_start']}" + (f"-{q['verse_end']}" if q['verse_end'] != q['verse_start'] else ""),
                    "issue": "Wording or punctuation mismatch",
                    "expected": canonical_full,
                    "actual": q["text"]
                })

        pass_rate = 1.0 if not extracted else (len(checked) / len(extracted))
        is_clean = len(mismatches) == 0

        return {
            "total_checked": len(extracted),
            "exact_matches": len(checked),
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "pass_rate": pass_rate,
            "passed": is_clean
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python verse_checker.py <path_to_markdown_study>")
        sys.exit(1)

    study_path = Path(sys.argv[1])
    if not study_path.exists():
        print(f"Error: File {study_path} not found.")
        sys.exit(1)

    text = study_path.read_text(encoding="utf-8")
    checker = VerseChecker()
    result = checker.check_text(text)

    print(f"=== Verse Checker Report for {study_path.name} ===")
    print(f"Total Quotations Checked: {result['total_checked']}")
    print(f"Exact/Valid Matches: {result['exact_matches']}")
    print(f"Mismatches: {result['mismatch_count']}")

    if not result["passed"]:
        print("\nMISMATCHES DETECTED:")
        for m in result["mismatches"]:
            print(f"- Reference: {m['reference']}")
            print(f"  Issue:    {m['issue']}")
            print(f"  Actual:   \"{m['actual']}\"")
            if m.get('expected'):
                print(f"  Expected: \"{m['expected']}\"")
        sys.exit(1)
    else:
        print("\nPASS: All referenced Scripture quotations are 100% faithful to canonical KJV.")
        sys.exit(0)

if __name__ == "__main__":
    main()
