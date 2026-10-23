"""
IncuBrix Engine — Deduplication & State Tracking Module
Uses SHA-256 content hashing and normalized token similarity stored in SQLite.
Guarantees repeat runs yield 0 duplicate assets and refresh runs only add new items.
"""

import hashlib
import os
import re
import sqlite3
from typing import Tuple, Optional


def normalize_text(text: str) -> str:
    """Normalize text by lowering, removing punctuation, and stripping extra whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())


def compute_content_hash(content: str) -> str:
    """Compute SHA-256 hash of normalized content string."""
    norm = normalize_text(content)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


class DedupStore:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            state_dir = os.path.join(base_dir, "state")
            os.makedirs(state_dir, exist_ok=True)
            db_path = os.path.join(state_dir, "engine_state.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS seen_assets (
                    asset_id TEXT PRIMARY KEY,
                    content_hash TEXT NOT NULL UNIQUE,
                    hook_normalized TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash ON seen_assets(content_hash)")
            conn.commit()

    def check_duplicate(self, content_text: str, hook_text: str) -> Tuple[bool, str]:
        """
        Check if content or hook already exists in the store.
        Returns (is_duplicate: bool, reason: str).
        """
        c_hash = compute_content_hash(content_text)
        norm_hook = normalize_text(hook_text)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 1. Exact content hash check
            cursor.execute("SELECT asset_id FROM seen_assets WHERE content_hash = ?", (c_hash,))
            row = cursor.fetchone()
            if row:
                return True, f"Exact content match with existing asset: {row[0]}"

            # 2. Exact or near-identical hook check
            cursor.execute("SELECT asset_id, hook_normalized FROM seen_assets")
            rows = cursor.fetchall()
            for existing_id, existing_hook in rows:
                if existing_hook == norm_hook:
                    return True, f"Identical hook text with asset: {existing_id}"
                # Word token Jaccard similarity
                s1 = set(norm_hook.split())
                s2 = set(existing_hook.split())
                if s1 and s2:
                    jaccard = len(s1 & s2) / len(s1 | s2)
                    if jaccard > 0.85:
                        return True, f"High hook similarity ({jaccard:.2f}) with asset: {existing_id}"

        return False, ""

    def record_asset(self, asset_id: str, content_text: str, hook_text: str, platform: str = "") -> bool:
        """Record an asset in the deduplication database."""
        c_hash = compute_content_hash(content_text)
        norm_hook = normalize_text(hook_text)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO seen_assets (asset_id, content_hash, hook_normalized, platform)
                    VALUES (?, ?, ?, ?)
                    """,
                    (asset_id, c_hash, norm_hook, platform),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def clear(self):
        """Clear all stored state (for testing)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM seen_assets")
            conn.commit()
