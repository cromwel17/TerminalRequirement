import os
import re

import customtkinter as ctk

from Literacy_data import LITERACY_DATABASE


class ThemeMixin:
    def theme_for(self, grade="4"):
        palettes = {
            "4": {
                "bg_color": "#0e1b16",
                "panel": "#12251d",
                "menu_bg": os.path.join(self.base_dir, "menu_bg.png"),
                "menu_shell": "#102219",
                "menu_card": "#173328",
                "menu_progress": "#1a2d25",
                "menu_button": "#8fd8b1",
                "menu_button_text": "#0b241a",
                "menu_delete": "#ff7a7a",
                "hero": "#1a3429",
                "card": "#183126",
                "hud_color": "#1c392c",
                "card_color": "#214334",
                "accent": "#98f5c3",
                "highlight": "#52c7ff",
                "highlight_hover": "#31b0eb",
                "light": "#f4fff8",
                "muted": "#c4ded0",
                "entry": "#11261d",
                "chip": "#244a39",
                "overlay": "#102219",
                "shadow": "#0a1511",
                "secondary": "#ccefd8",
                "secondary_hover": "#b8e9ca",
                "secondary_text": "#143323",
                "button_text": "#072033",
                "shell_tint": "transparent",
                "panel_edge": "#3a6d55",
                "soft_line": "#487860",
                "hero_text": "#f5fff8",
                "question_glow": "#183529",
                "input_fill": "#173127",
                "forest": "#29513e",
                "forest_accent": "#b7f0c8",
                "volcano": "#4f210f",
                "volcano_accent": "#ffaf1a",
                "cyber": "#24344d",
                "cyber_accent": "#52c7ff",
                "bg_image": os.path.join(self.base_dir, "forest_bg.jpg"),
            },
            "5": {
                "bg_color": "#24110b",
                "panel": "#2d1710",
                "menu_bg": os.path.join(self.base_dir, "menu_bg.png"),
                "menu_shell": "#22140e",
                "menu_card": "#3a1f14",
                "menu_progress": "#2f1d15",
                "menu_button": "#ffb457",
                "menu_button_text": "#3c1d00",
                "menu_delete": "#ff7a7a",
                "hero": "#462112",
                "card": "#3b190f",
                "hud_color": "#4f2312",
                "card_color": "#71331b",
                "accent": "#ffd166",
                "highlight": "#ff8a4c",
                "highlight_hover": "#ff7730",
                "light": "#fff7f2",
                "muted": "#f0c7b5",
                "entry": "#31160d",
                "chip": "#713018",
                "overlay": "#26120a",
                "shadow": "#180a06",
                "secondary": "#ffd8a8",
                "secondary_hover": "#ffc97d",
                "secondary_text": "#532400",
                "button_text": "#3b1b00",
                "shell_tint": "transparent",
                "panel_edge": "#904726",
                "soft_line": "#a25a31",
                "hero_text": "#fff7f2",
                "question_glow": "#412010",
                "input_fill": "#3a1a10",
                "forest": "#29513e",
                "forest_accent": "#b7f0c8",
                "volcano": "#7b3113",
                "volcano_accent": "#ffb000",
                "cyber": "#24344d",
                "cyber_accent": "#52c7ff",
                "bg_image": os.path.join(self.base_dir, "volcano_bg.jpg"),
            },
            "6": {
                "bg_color": "#0a1221",
                "panel": "#101d31",
                "menu_bg": os.path.join(self.base_dir, "menu_bg.png"),
                "menu_shell": "#0f1b2e",
                "menu_card": "#16293f",
                "menu_progress": "#142436",
                "menu_button": "#78d6ff",
                "menu_button_text": "#072033",
                "menu_delete": "#ff7a7a",
                "hero": "#132946",
                "card": "#13263f",
                "hud_color": "#1a3150",
                "card_color": "#23425f",
                "accent": "#77ddff",
                "highlight": "#52c7ff",
                "highlight_hover": "#31b0eb",
                "light": "#f3f8ff",
                "muted": "#b9c9e4",
                "entry": "#0d1a2d",
                "chip": "#1e3556",
                "overlay": "#0d1628",
                "shadow": "#07101c",
                "secondary": "#d9f3ff",
                "secondary_hover": "#c5ebff",
                "secondary_text": "#08223b",
                "button_text": "#072033",
                "shell_tint": "transparent",
                "panel_edge": "#3c668f",
                "soft_line": "#4b79a3",
                "hero_text": "#f3f8ff",
                "question_glow": "#142a44",
                "input_fill": "#13253a",
                "forest": "#29513e",
                "forest_accent": "#b7f0c8",
                "volcano": "#7b3113",
                "volcano_accent": "#ffb000",
                "cyber": "#324866",
                "cyber_accent": "#52c7ff",
                "bg_image": os.path.join(self.base_dir, "cyber_bg.jpg"),
            },
        }
        return palettes.get(grade, palettes["4"])

    def current_theme(self):
        return self.theme_for(self.current_grade if self.story_order else "4")

    def set_background(self, path):
        self.bg_path = path if path and os.path.exists(path) else None
        if not self.bg_path:
            return
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_label.lower()
        self.refresh_background()

    def refresh_background(self):
        if not self.bg_label or not self.bg_path:
            return
        try:
            from PIL import Image

            size = (max(self.winfo_width(), 860), max(self.winfo_height(), 640))
            if size == self.bg_size:
                return
            image = Image.open(self.bg_path).resize(size)
            self.bg_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            self.bg_label.configure(image=self.bg_image)
            self.bg_size = size
        except Exception:
            self.bg_label.configure(image=None)


class AnswerCheckMixin:
    def answer_spec(self, correct_answer):
        if isinstance(correct_answer, dict):
            return correct_answer
        if isinstance(correct_answer, (list, tuple, set)):
            return {"mode": "any", "answers": [str(answer) for answer in correct_answer]}
        return {"mode": "exact", "answers": [str(correct_answer)]}

    def normalize_answer(self, text):
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s-]", " ", text)
        text = text.replace("-", " ")
        return re.sub(r"\s+", " ", text).strip()

    def singularize_word(self, word):
        if word.endswith("ies") and len(word) > 3:
            return word[:-3] + "y"
        if word.endswith("oes") and len(word) > 3:
            return word[:-2]
        if word.endswith("ses") and len(word) > 3:
            return word[:-2]
        if word.endswith("s") and len(word) > 3 and not word.endswith(("ss", "us", "is")):
            return word[:-1]
        return word

    def answer_tokens(self, text):
        return [self.singularize_word(token) for token in self.normalize_answer(text).split() if token]

    def accepted_answers(self, correct_answer):
        spec = self.answer_spec(correct_answer)
        return [str(answer) for answer in spec["answers"]]

    def is_correct_answer(self, user_answer, correct_answer):
        user_normalized = self.normalize_answer(user_answer)
        user_tokens = set(self.answer_tokens(user_answer))
        if not user_normalized:
            return False

        spec = self.answer_spec(correct_answer)
        expected_answers = self.accepted_answers(correct_answer)
        matched = 0

        for expected in expected_answers:
            expected_normalized = self.normalize_answer(expected)
            expected_tokens = set(self.answer_tokens(expected))
            if user_normalized == expected_normalized:
                matched += 1
                continue
            if expected_normalized and expected_normalized in user_normalized:
                matched += 1
                continue
            if user_tokens and expected_tokens and (
                expected_tokens.issubset(user_tokens) or user_tokens.issubset(expected_tokens)
            ):
                matched += 1

        if spec["mode"] == "all":
            return matched >= len(expected_answers)
        return matched > 0


class MissionStateMixin:
    def reset_state(self):
        self.player_name = "Pilot-01"
        self.current_grade = "4"
        self.story_order = []
        self.story_idx = 0
        self.q_idx = 0
        self.score = 0
        self.xp = 0
        self.rank = "Novice Pilot"
        self.timer_seconds = 30
        self.timer_id = None
        self.paused = False
        self.reviewing_previous = False
        self.blur_overlay = None
        self.question_history = []

    def mission_payload(self):
        return {
            "grade": self.current_grade,
            "story_idx": self.story_idx,
            "q_idx": self.q_idx,
            "score": self.score,
            "xp": self.xp,
            "rank": self.rank,
            "timer_seconds": self.timer_seconds,
            "story_order": self.story_order,
        }

    def current_story(self):
        return LITERACY_DATABASE[self.current_grade][self.story_order[self.story_idx]]

    def update_rank(self):
        if self.xp >= 2000:
            self.rank = "Elite Commander"
        elif self.xp >= 1500:
            self.rank = "Squad Leader"
        elif self.xp >= 1000:
            self.rank = "Senior Pilot"
        elif self.xp >= 500:
            self.rank = "Junior Pilot"
        else:
            self.rank = "Novice Pilot"

    def total_questions(self):
        return sum(len(story["qs"]) for story in LITERACY_DATABASE[self.current_grade])

    def mission_grade(self, score, total_questions):
        percent = (score / total_questions) * 100 if total_questions else 0
        if percent >= 90:
            return "S"
        if percent >= 80:
            return "A"
        if percent >= 70:
            return "B"
        if percent >= 60:
            return "C"
        return "D"

    def result_summary(self):
        total_questions = self.total_questions() if self.story_order else 30
        return {
            "score": self.score,
            "total_questions": total_questions,
            "xp_earned": self.score * 100,
            "mission_grade": self.mission_grade(self.score, total_questions),
            "rank": self.rank,
        }
