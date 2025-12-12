import os
import json
import datetime


class HistoryManager:
    def __init__(self, history_file="agent_history.json"):
        self.history_file = history_file
        self._init_storage()

    # Ensure file exists and valid
    def _init_storage(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def load_history(self):
        """Load history from file safely"""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Reset file if corrupted
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            return []

    def save_entry(self, input_text, mode, final_report):
        """Save a research result with timestamp"""
        history = self.load_history()

        # Safety truncation to avoid huge storage
        input_text = input_text[:500] + "..." if len(input_text) > 500 else input_text
        final_report = final_report[:5000] + "..." if len(final_report) > 5000 else final_report

        entry = {
            "id": len(history) + 1,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mode": mode,
            "input": input_text,
            "report": final_report,
        }

        history.append(entry)

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

        return entry

    def clear_history(self):
        """Remove all saved history"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    def delete_entry(self, entry_id):
        """Delete a specific history record by id"""
        history = self.load_history()
        new_history = [h for h in history if h["id"] != entry_id]

        # Re-index IDs
        for i, item in enumerate(new_history):
            item["id"] = i + 1

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(new_history, f, indent=4)

        return True
