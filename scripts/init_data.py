#!/usr/bin/env python3
"""
Initialize Bible structure and canonical KJV indexing.
Generates data/books.json and initial progress/progress.json.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROGRESS_DIR = BASE_DIR / "progress"

BOOK_NAMES = [
    # Old Testament (1-39)
    (1, "Genesis", "Gen", "OT", 50),
    (2, "Exodus", "Exod", "OT", 40),
    (3, "Leviticus", "Lev", "OT", 27),
    (4, "Numbers", "Num", "OT", 36),
    (5, "Deuteronomy", "Deut", "OT", 34),
    (6, "Joshua", "Josh", "OT", 24),
    (7, "Judges", "Judg", "OT", 21),
    (8, "Ruth", "Ruth", "OT", 4),
    (9, "1 Samuel", "1Sam", "OT", 31),
    (10, "2 Samuel", "2Sam", "OT", 24),
    (11, "1 Kings", "1Kgs", "OT", 22),
    (12, "2 Kings", "2Kgs", "OT", 25),
    (13, "1 Chronicles", "1Chr", "OT", 29),
    (14, "2 Chronicles", "2Chr", "OT", 36),
    (15, "Ezra", "Ezra", "OT", 10),
    (16, "Nehemiah", "Neh", "OT", 13),
    (17, "Esther", "Esth", "OT", 10),
    (18, "Job", "Job", "OT", 42),
    (19, "Psalms", "Ps", "OT", 150),
    (20, "Proverbs", "Prov", "OT", 31),
    (21, "Ecclesiastes", "Eccl", "OT", 12),
    (22, "Song of Solomon", "Song", "OT", 8),
    (23, "Isaiah", "Isa", "OT", 66),
    (24, "Jeremiah", "Jer", "OT", 52),
    (25, "Lamentations", "Lam", "OT", 5),
    (26, "Ezekiel", "Ezek", "OT", 48),
    (27, "Daniel", "Dan", "OT", 12),
    (28, "Hosea", "Hos", "OT", 14),
    (29, "Joel", "Joel", "OT", 3),
    (30, "Amos", "Amos", "OT", 9),
    (31, "Obadiah", "Obad", "OT", 1),
    (32, "Jonah", "Jonah", "OT", 4),
    (33, "Micah", "Mic", "OT", 7),
    (34, "Nahum", "Nah", "OT", 3),
    (35, "Habakkuk", "Hab", "OT", 3),
    (36, "Zephaniah", "Zeph", "OT", 3),
    (37, "Haggai", "Hag", "OT", 2),
    (38, "Zechariah", "Zech", "OT", 14),
    (39, "Malachi", "Mal", "OT", 4),
    # New Testament (40-66)
    (40, "Matthew", "Matt", "NT", 28),
    (41, "Mark", "Mark", "NT", 16),
    (42, "Luke", "Luke", "NT", 24),
    (43, "John", "John", "NT", 21),
    (44, "Acts", "Acts", "NT", 28),
    (45, "Romans", "Rom", "NT", 16),
    (46, "1 Corinthians", "1Cor", "NT", 16),
    (47, "2 Corinthians", "2Cor", "NT", 13),
    (48, "Galatians", "Gal", "NT", 6),
    (49, "Ephesians", "Eph", "NT", 6),
    (50, "Philippians", "Phil", "NT", 4),
    (51, "Colossians", "Col", "NT", 4),
    (52, "1 Thessalonians", "1Thess", "NT", 5),
    (53, "2 Thessalonians", "2Thess", "NT", 3),
    (54, "1 Timothy", "1Tim", "NT", 6),
    (55, "2 Timothy", "2Tim", "NT", 4),
    (56, "Titus", "Titus", "NT", 3),
    (57, "Philemon", "Phlm", "NT", 1),
    (58, "Hebrews", "Heb", "NT", 13),
    (59, "James", "Jas", "NT", 5),
    (60, "1 Peter", "1Pet", "NT", 5),
    (61, "2 Peter", "2Pet", "NT", 3),
    (62, "1 John", "1John", "NT", 5),
    (63, "2 John", "2John", "NT", 1),
    (64, "3 John", "3John", "NT", 1),
    (65, "Jude", "Jude", "NT", 1),
    (66, "Revelation", "Rev", "NT", 22),
]

def main():
    kjv_file = DATA_DIR / "kjv.json"
    if not kjv_file.exists():
        raise FileNotFoundError(f"{kjv_file} does not exist. Run curl to download it first.")

    with open(kjv_file, "r", encoding="utf-8") as f:
        kjv_raw = json.load(f)

    rows = kjv_raw.get("resultset", {}).get("row", [])

    # Index verses by book_id -> chapter -> verse -> text
    bible_index = {}
    for r in rows:
        field = r.get("field", [])
        if len(field) >= 5:
            # [id, book_id, chapter, verse, text]
            _, b_id, ch, v, text = field[:5]
            bible_index.setdefault(b_id, {}).setdefault(ch, {})[v] = text

    books_meta = []
    total_chapters = 0
    total_verses = 0

    chapter_manifest = []

    for b_id, name, abbr, testament, expected_ch in BOOK_NAMES:
        ch_dict = bible_index.get(b_id, {})
        actual_ch_count = len(ch_dict)
        if actual_ch_count != expected_ch:
            print(f"Warning: {name} expected {expected_ch} chapters, found {actual_ch_count}")

        book_verses = sum(len(v_dict) for v_dict in ch_dict.values())
        total_chapters += actual_ch_count
        total_verses += book_verses

        b_entry = {
            "book_id": b_id,
            "name": name,
            "abbr": abbr,
            "testament": testament,
            "chapter_count": actual_ch_count,
            "verse_count": book_verses,
            "chapters": {}
        }

        for ch_num in range(1, actual_ch_count + 1):
            verses = ch_dict.get(ch_num, {})
            b_entry["chapters"][str(ch_num)] = len(verses)

            clean_book = name.replace(" ", "_")
            file_rel_path = f"studies/{testament}/{b_id:02d}_{clean_book}/{clean_book}_{ch_num:02d}.md"

            chapter_manifest.append({
                "book_id": b_id,
                "book_name": name,
                "chapter": ch_num,
                "verse_count": len(verses),
                "testament": testament,
                "output_path": file_rel_path,
                "status": "pending",  # pending | in_progress | completed | failed
                "iterations": 0,
                "laya_score": None,
                "verse_mismatches": None,
                "last_run": None,
            })

        books_meta.append(b_entry)

    # Save data/books.json
    with open(DATA_DIR / "books.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_books": len(books_meta),
            "total_chapters": total_chapters,
            "total_verses": total_verses,
            "books": books_meta
        }, f, indent=2)

    # Save progress/progress.json
    progress_file = PROGRESS_DIR / "progress.json"
    if not progress_file.exists():
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump({
                "schema_version": "1.0",
                "total_chapters": total_chapters,
                "completed": 0,
                "failed": 0,
                "pending": total_chapters,
                "chapters": chapter_manifest
            }, f, indent=2)
        print(f"Created new {progress_file}")
    else:
        print(f"{progress_file} already exists, leaving intact.")

    print(f"Initialization complete: {len(books_meta)} books, {total_chapters} chapters, {total_verses} verses indexed.")

if __name__ == "__main__":
    main()
