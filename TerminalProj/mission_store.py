import csv
import json
import os


USER_FIELDS = ["username", "password"]
PROGRESS_FIELDS = [
    "username",
    "grade",
    "story_idx",
    "q_idx",
    "score",
    "xp",
    "rank",
    "timer_seconds",
    "story_order",
]


class MissionStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.users_file = os.path.join(base_dir, "users.csv")
        self.progress_file = os.path.join(base_dir, "progress.csv")
        self.logs_file = os.path.join(base_dir, "mission_logs.txt")
        self.ensure_files()

    def ensure_files(self):
        self._ensure_csv(self.users_file, USER_FIELDS)
        self._ensure_csv(self.progress_file, PROGRESS_FIELDS)

    def _ensure_csv(self, path, fields):
        if os.path.exists(path):
            return
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

    def _read_csv(self, path):
        with open(path, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _write_csv(self, path, fields, rows):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def find_user(self, username):
        target = username.strip().lower()
        for row in self._read_csv(self.users_file):
            if row["username"].strip().lower() == target:
                return row
        return None

    def register_user(self, username, password):
        if self.find_user(username):
            return False
        with open(self.users_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
            writer.writerow({"username": username, "password": password})
        return True

    def validate_user(self, username, password):
        user = self.find_user(username)
        return bool(user and user["password"] == password)

    def get_progress(self, username):
        for row in self._read_csv(self.progress_file):
            if row["username"] == username:
                row["story_idx"] = int(row["story_idx"])
                row["q_idx"] = int(row["q_idx"])
                row["score"] = int(row["score"])
                row["xp"] = int(row["xp"])
                row["timer_seconds"] = int(row["timer_seconds"])
                row["story_order"] = json.loads(row["story_order"]) if row["story_order"] else []
                return row
        return None

    def save_progress(self, username, payload):
        rows = [row for row in self._read_csv(self.progress_file) if row["username"] != username]
        rows.append(
            {
                "username": username,
                "grade": payload["grade"],
                "story_idx": payload["story_idx"],
                "q_idx": payload["q_idx"],
                "score": payload["score"],
                "xp": payload["xp"],
                "rank": payload["rank"],
                "timer_seconds": payload["timer_seconds"],
                "story_order": json.dumps(payload["story_order"]),
            }
        )
        self._write_csv(self.progress_file, PROGRESS_FIELDS, rows)

    def delete_progress(self, username):
        rows = [row for row in self._read_csv(self.progress_file) if row["username"] != username]
        self._write_csv(self.progress_file, PROGRESS_FIELDS, rows)

    def log_result(self, player_name, grade, score):
        with open(self.logs_file, "a", encoding="utf-8") as file:
            file.write(f"Pilot: {player_name} | Grade: {grade} | Score: {score}/30\n")
