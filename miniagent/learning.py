"""
Conversation logging and SFT dataset extraction for continuous learning.

Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Optional

DEFAULT_CONV_PATH = Path.home() / ".miniagent" / "conversations.jsonl"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_dataset_path() -> Path:
    """Default output: ``<repo>/dataset/learned_sft.jsonl``."""
    return _repo_root() / "dataset" / "learned_sft.jsonl"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    _ensure_parent(path)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    try:
        import fcntl  # Unix: avoid interleaved lines from concurrent writers

        with open(path, "a", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(line)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except (ImportError, OSError):
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    if not path.is_file():
        return
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    yield obj
                else:
                    print(
                        f"warning: skipping non-object JSON on line {line_no}",
                        file=sys.stderr,
                    )
            except json.JSONDecodeError as e:
                print(
                    f"warning: invalid JSON on line {line_no}: {e}",
                    file=sys.stderr,
                )


def _normalize_for_dedup(user_text: str) -> str:
    """Lightweight normalization for duplicate detection (no extra deps)."""
    s = user_text.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


class ConversationLogger:
    """
    Append-only JSONL logger for user/assistant turns.

    Default file: ``~/.miniagent/conversations.jsonl``
    """

    def __init__(
        self,
        path: Optional[os.PathLike[str] | str] = None,
        session_id: Optional[str] = None,
    ) -> None:
        self.path = Path(path) if path is not None else DEFAULT_CONV_PATH
        self.session_id = session_id if session_id is not None else str(uuid.uuid4())

    def log(
        self,
        user_msg: str,
        assistant_msg: str,
        feedback: Optional[int] = None,
    ) -> None:
        entry: dict[str, Any] = {
            "timestamp": _iso_now(),
            "user": user_msg,
            "assistant": assistant_msg,
            "feedback": feedback,
            "session_id": self.session_id,
        }
        _append_jsonl(self.path, entry)

    def rate(self, session_id: str, rating: int) -> int:
        """
        Set star rating (1–5) on all turns for ``session_id``.

        Returns the number of records updated.
        """
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not self.path.is_file():
            return 0

        lines: list[str] = []
        updated = 0
        with open(self.path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    lines.append(raw.rstrip("\n"))
                    continue
                if not isinstance(obj, dict):
                    lines.append(raw.rstrip("\n"))
                    continue
                if obj.get("session_id") == session_id:
                    obj["feedback"] = rating
                    updated += 1
                lines.append(json.dumps(obj, ensure_ascii=False))

        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        os.replace(tmp, self.path)
        return updated


def extract_sft_data(
    min_rating: int = 3,
    conversations_path: Optional[os.PathLike[str] | str] = None,
    output_path: Optional[os.PathLike[str] | str] = None,
) -> int:
    """
    Read conversation JSONL, filter by rating rules, dedupe by normalized user text,
    write ``{"user": ..., "assistant": ...}`` lines to the dataset path.

    - Rows with ``feedback is None``: always included (no rating to filter).
    - Rows with numeric ``feedback``: included only if ``feedback >= min_rating``.

    Returns the number of pairs written.
    """
    conv_path = Path(conversations_path) if conversations_path else DEFAULT_CONV_PATH
    out_path = Path(output_path) if output_path else default_dataset_path()

    _ensure_parent(out_path)

    seen: set[str] = set()
    count = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for row in _iter_jsonl(conv_path):
            user = row.get("user")
            assistant = row.get("assistant")
            if not isinstance(user, str) or not isinstance(assistant, str):
                continue
            fb = row.get("feedback")
            if fb is not None:
                try:
                    r = int(fb)
                except (TypeError, ValueError):
                    continue
                if r < min_rating:
                    continue

            key = _normalize_for_dedup(user)
            if key in seen:
                continue
            seen.add(key)
            rec = {"user": user, "assistant": assistant}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1

    return count


def _conversation_stats(path: Path) -> dict[str, Any]:
    total = 0
    sessions: set[str] = set()
    ratings: list[int] = []
    first_ts: Optional[str] = None
    last_ts: Optional[str] = None

    for row in _iter_jsonl(path):
        total += 1
        sid = row.get("session_id")
        if isinstance(sid, str):
            sessions.add(sid)
        ts = row.get("timestamp")
        if isinstance(ts, str):
            if first_ts is None or ts < first_ts:
                first_ts = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts
        fb = row.get("feedback")
        if fb is not None:
            try:
                ratings.append(int(fb))
            except (TypeError, ValueError):
                pass

    with_feedback = len(ratings)
    avg = sum(ratings) / len(ratings) if ratings else None

    return {
        "path": str(path),
        "total_turns": total,
        "unique_sessions": len(sessions),
        "turns_with_feedback": with_feedback,
        "average_rating": avg,
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
    }


def _cmd_log(path: Path) -> int:
    if not path.is_file():
        print(f"No conversation file at {path}")
        return 0
    stats = _conversation_stats(path)
    print(f"File:           {stats['path']}")
    print(f"Total turns:    {stats['total_turns']}")
    print(f"Sessions:       {stats['unique_sessions']}")
    print(f"With feedback:  {stats['turns_with_feedback']}")
    if stats["average_rating"] is not None:
        print(f"Avg rating:     {stats['average_rating']:.2f}")
    else:
        print("Avg rating:     n/a")
    print(f"First timestamp: {stats['first_timestamp']}")
    print(f"Last timestamp:  {stats['last_timestamp']}")
    return 0


def _cmd_extract(args: argparse.Namespace) -> int:
    n = extract_sft_data(
        min_rating=args.min_rating,
        conversations_path=args.conversations,
        output_path=args.output,
    )
    out = Path(args.output) if args.output else default_dataset_path()
    print(f"Wrote {n} user/assistant pairs to {out}")
    return 0


def _cmd_clear(path: Path) -> int:
    if path.is_file():
        path.unlink()
        print(f"Cleared {path}")
    else:
        print(f"No file at {path} (nothing to clear)")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m miniagent.learning",
        description="MiniAgent conversation logging and SFT extraction",
    )
    p.add_argument(
        "--conversations",
        type=Path,
        default=DEFAULT_CONV_PATH,
        help=f"path to conversations JSONL (default: {DEFAULT_CONV_PATH})",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("log", help="show conversation stats")

    p_extract = sub.add_parser("extract", help="extract SFT data from conversations")
    p_extract.add_argument(
        "--min-rating",
        type=int,
        default=3,
        help="minimum star rating when feedback is present (default: 3)",
    )
    p_extract.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"output JSONL (default: {default_dataset_path()})",
    )

    sub.add_parser("clear", help="remove the conversations JSONL file")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = _build_parser()
    args = parser.parse_args(argv)

    conv_path: Path = args.conversations

    if args.command == "log":
        return _cmd_log(conv_path)
    if args.command == "extract":
        return _cmd_extract(args)
    if args.command == "clear":
        return _cmd_clear(conv_path)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
