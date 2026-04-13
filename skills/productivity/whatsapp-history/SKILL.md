# WhatsApp History

Search and browse WhatsApp message history from JSONL logs.

All WhatsApp messages (including untagged group messages) are logged to `$HERMES_HOME/logs/whatsapp/{chatId}.jsonl`.

## Usage

Use the `search_history.py` script to query logs:

```bash
# Last N messages from a chat
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --last 20

# Search by keyword
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --search "keyword"

# Filter by sender name
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --from "João"

# Messages from today
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --today

# Messages from a specific date
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --date 2026-04-10

# Combine filters
python3 $HERMES_HOME/../opt/hermes/skills/productivity/whatsapp-history/scripts/search_history.py --chat CHAT_ID --from "Ivan" --search "meeting" --last 50
```

You can also use standard shell tools directly on the JSONL files:

```bash
# List available chat logs
ls $HERMES_HOME/logs/whatsapp/

# Tail recent messages
tail -20 $HERMES_HOME/logs/whatsapp/CHAT_ID.jsonl | python3 -c "import sys,json; [print(f'[{json.loads(l).get(\"sender\",\"?\")}] {json.loads(l).get(\"body\",\"\")}') for l in sys.stdin]"

# Grep for keyword
grep -i "keyword" $HERMES_HOME/logs/whatsapp/CHAT_ID.jsonl
```

## Log Format

Each line is a JSON object:
```json
{"ts": 1712345678, "sender": "João", "senderId": "351918011685@s.whatsapp.net", "body": "message text", "chatId": "120363...@g.us", "isGroup": true}
```

Messages with media include additional fields:
```json
{"ts": 1712345678, "sender": "João", "body": "check this", "mediaType": "image", "mediaUrls": ["/path/to/cached/img.jpg"], ...}
```
