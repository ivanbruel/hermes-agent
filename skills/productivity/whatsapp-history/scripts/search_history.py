#!/usr/bin/env python3
"""Search WhatsApp JSONL message logs."""

import argparse
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path


def get_log_dir():
    hermes_home = os.getenv("HERMES_HOME", os.path.expanduser("~/.hermes"))
    return Path(hermes_home) / "logs" / "whatsapp"


def parse_args():
    parser = argparse.ArgumentParser(description="Search WhatsApp message history")
    parser.add_argument("--chat", help="Chat ID (filename without .jsonl)")
    parser.add_argument("--last", type=int, help="Show last N messages")
    parser.add_argument("--search", help="Search for keyword (case-insensitive)")
    parser.add_argument("--sender", "--from", dest="sender", help="Filter by sender name")
    parser.add_argument("--today", action="store_true", help="Messages from today")
    parser.add_argument("--date", help="Messages from specific date (YYYY-MM-DD)")
    parser.add_argument("--list", action="store_true", help="List available chat logs")
    return parser.parse_args()


def list_chats(log_dir):
    if not log_dir.exists():
        print("No logs directory found.")
        return
    for f in sorted(log_dir.glob("*.jsonl")):
        lines = sum(1 for _ in open(f))
        print(f"  {f.stem}  ({lines} messages)")


def search(log_dir, args):
    if not args.chat:
        print("Error: --chat is required (use --list to see available chats)")
        sys.exit(1)

    log_file = log_dir / f"{args.chat}.jsonl"
    if not log_file.exists():
        # Try with common suffixes
        candidates = list(log_dir.glob(f"*{args.chat}*"))
        if len(candidates) == 1:
            log_file = candidates[0]
        elif candidates:
            print(f"Multiple matches for '{args.chat}':")
            for c in candidates:
                print(f"  {c.stem}")
            sys.exit(1)
        else:
            print(f"No log file found for chat: {args.chat}")
            sys.exit(1)

    # Read all lines
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Parse
    messages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            messages.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    # Filter by date
    if args.today:
        today = date.today()
        messages = [m for m in messages if datetime.fromtimestamp(m.get("ts", 0)).date() == today]
    elif args.date:
        try:
            target = date.fromisoformat(args.date)
        except ValueError:
            print(f"Invalid date format: {args.date} (use YYYY-MM-DD)")
            sys.exit(1)
        messages = [m for m in messages if datetime.fromtimestamp(m.get("ts", 0)).date() == target]

    # Filter by sender
    if args.sender:
        needle = args.sender.lower()
        messages = [m for m in messages if needle in m.get("sender", "").lower()]

    # Filter by keyword
    if args.search:
        needle = args.search.lower()
        messages = [m for m in messages if needle in m.get("body", "").lower()]

    # Limit
    if args.last:
        messages = messages[-args.last:]

    # Output
    if not messages:
        print("No messages found.")
        return

    for m in messages:
        ts = m.get("ts", 0)
        time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M") if ts else "??:??"
        sender = m.get("sender", "?")
        body = m.get("body", "")
        media = ""
        if m.get("mediaType"):
            media = f" [{m['mediaType']}]"
        print(f"[{time_str}] {sender}: {body}{media}")


def main():
    args = parse_args()
    log_dir = get_log_dir()

    if args.list:
        list_chats(log_dir)
    else:
        search(log_dir, args)


if __name__ == "__main__":
    main()
