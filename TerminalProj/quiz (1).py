import os
import random

import customtkinter as ctk

from Literacy_data import LITERACY_DATABASE
from app_mixins import AnswerCheckMixin, MissionStateMixin, ThemeMixin
from mission_screens import AuthScreen, MenuScreen, MissionScreen, ResultScreen
from mission_store import MissionStore


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LiteracyMissionControl(ThemeMixin, AnswerCheckMixin, MissionStateMixin, ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Elementary Functional Literacy v3.0")
        self.geometry("1100x760")
        self.minsize(860, 640)

        self.base_dir = os.path.dirname(__file__)
        self.store = MissionStore(self.base_dir)
        self.current_user = None
        self.active_screen = None
        self.bg_label = None
        self.bg_image = None
        self.bg_path = None
        self.bg_size = (0, 0)

        self.reset_state()
        self.bind("<Configure>", self.on_resize)
        self.show_auth_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.active_screen = None
        self.bg_label = None
        self.bg_image = None
        self.bg_size = (0, 0)

    def mount(self, screen_class, *args):
        self.clear_screen()
        theme = self.current_theme()
        self.configure(fg_color=theme["bg_color"])
        screen = screen_class(self, theme, *args)
        screen.pack(fill="both", expand=True)
        self.active_screen = screen
        return screen

    def on_resize(self, event):
        if event.widget != self:
            return
        self.refresh_background()
        if self.active_screen:
            self.active_screen.on_resize()

    def login_user(self, username, password, screen):
        if not username or not password:
            screen.show_message("Enter both username and password.", "#ff7a7a")
            return
        if not self.store.validate_user(username, password):
            screen.show_message("Invalid username or password.", "#ff7a7a")
            return
        self.current_user = username
        self.player_name = username
        self.show_main_menu()

    def register_user(self, username, password, screen):
        if not username or not password:
            screen.show_message("Enter both username and password.", "#ff7a7a")
            return
        if not self.store.register_user(username, password):
            screen.show_message("Username already exists.", "#ff7a7a")
            return
        screen.show_message("Registration complete. You can now log in.", "#7cf29a")

    def logout(self):
        self.current_user = None
        self.reset_state()
        self.show_auth_screen()

    def show_auth_screen(self):
        self.reset_state()
        self.mount(AuthScreen)

    def show_main_menu(self):
        progress = self.store.get_progress(self.current_user) if self.current_user else None
        screen = self.mount(MenuScreen, self.current_user, progress)
        return screen

    def start_new_mission(self, grade):
        self.reset_state()
        self.player_name = self.current_user or "Pilot-01"
        self.current_grade = grade
        self.story_order = list(range(len(LITERACY_DATABASE[grade])))
        random.shuffle(self.story_order)
        self.show_mission_ui()

    def load_progress(self):
        progress = self.store.get_progress(self.current_user)
        if not progress:
            if self.active_screen:
                self.active_screen.show_message("No saved progress found.", "#ff7a7a")
            return
        self.reset_state()
        self.player_name = self.current_user
        self.current_grade = progress["grade"]
        self.story_idx = progress["story_idx"]
        self.q_idx = progress["q_idx"]
        self.score = progress["score"]
        self.xp = progress["xp"]
        self.rank = progress["rank"]
        self.timer_seconds = progress["timer_seconds"]
        self.story_order = progress["story_order"]
        self.show_mission_ui()

    def delete_save_from_menu(self):
        if not self.store.get_progress(self.current_user):
            if self.active_screen:
                self.active_screen.show_message("No saved progress to delete.", "#ff7a7a")
            return
        self.store.delete_progress(self.current_user)
        self.show_main_menu().show_message("Saved progress deleted.", "#7cf29a")


    def show_mission_ui(self):
        story = self.current_story()
        question_text, answer = story["qs"][self.q_idx]
        self.mount(
            MissionScreen,
            {
                "player_name": self.player_name,
                "story_idx": self.story_idx,
                "rank": self.rank,
                "xp": self.xp,
                "timer_seconds": self.timer_seconds,
            },
            story["story"],
            question_text,
            answer,
        )
        self.update_timer()

    def save_progress(self):
        if self.current_user and self.story_order:
            self.store.save_progress(self.current_user, self.mission_payload())

    def cancel_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer(self):
        if self.paused or not isinstance(self.active_screen, MissionScreen):
            return
        self.active_screen.update_timer(self.timer_seconds)
        if self.timer_seconds <= 0:
            self.active_screen.set_feedback("Time's up! Auto-skipping...", "#ff7a7a")
            self.after(1000, self.next_question)
            return
        self.timer_seconds -= 1
        self.timer_id = self.after(1000, self.update_timer)

    def process_answer(self, correct_answer):
        if self.paused or not isinstance(self.active_screen, MissionScreen):
            return
        answer = self.active_screen.answer_entry.get().strip()
        if self.is_correct_answer(answer, correct_answer):
            old_rank = self.rank
            self.score += 1
            self.xp += 100
            self.update_rank()
            message = f"Level Up! New Rank: {self.rank}" if old_rank != self.rank else "Correct! +100 XP"
            color = "#ffd166" if old_rank != self.rank else "#7cf0ff"
            self.active_screen.set_feedback(message, color)
        else:
            accepted = ", ".join(self.accepted_answers(correct_answer))
            self.active_screen.set_feedback(f"Incorrect! Correct answer: {accepted}", "#ff7a7a")
        self.active_screen.update_rank(self.xp, self.rank)
        self.after(1200, self.next_question)

    def skip_question(self):
        if self.paused or not isinstance(self.active_screen, MissionScreen):
            return
        self.active_screen.set_feedback("Question skipped.", "#ffd166")
        self.after(800, self.next_question)

    def next_question(self):
        self.cancel_timer()
        self.q_idx += 1
        if self.q_idx >= len(self.current_story()["qs"]):
            self.q_idx = 0
            self.story_idx += 1
        if self.story_idx >= len(self.story_order):
            self.end_mission()
            return
        self.timer_seconds = 30
        self.show_mission_ui()

    def pause_quiz(self):
        if self.paused or not isinstance(self.active_screen, MissionScreen):
            return
        self.paused = True
        self.cancel_timer()
        self.blur_overlay = ctk.CTkFrame(self, fg_color="#000000")
        self.blur_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(self.blur_overlay, corner_radius=28, fg_color=self.current_theme()["panel"])
        card.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text="Paused", font=("Orbitron", 34, "bold"), text_color=self.current_theme()["highlight"]).pack(padx=44, pady=(28, 10))
        ctk.CTkLabel(card, text="Take a breath, then resume or save and head back to menu.", font=("Arial", 14), text_color=self.current_theme()["muted"]).pack(padx=30)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=(20, 30))
        ctk.CTkButton(row, text="Resume", width=170, height=44, corner_radius=14, fg_color=self.current_theme()["highlight"], hover_color=self.current_theme()["highlight_hover"], text_color=self.current_theme()["button_text"], command=self.resume_quiz).pack(side="left", padx=6)
        ctk.CTkButton(row, text="Save & Menu", width=170, height=44, corner_radius=14, fg_color=self.current_theme()["secondary"], hover_color=self.current_theme()["secondary_hover"], text_color=self.current_theme()["secondary_text"], command=self.handle_save_and_menu).pack(side="left", padx=6)

    def resume_quiz(self):
        if not self.paused:
            return
        self.paused = False
        if self.blur_overlay:
            self.blur_overlay.destroy()
            self.blur_overlay = None
        self.update_timer()

    def handle_save_and_menu(self):
        self.paused = False
        self.cancel_timer()
        if self.blur_overlay:
            self.blur_overlay.destroy()
            self.blur_overlay = None
        self.save_progress()
        self.show_main_menu().show_message("Progress saved successfully.", "#7cf29a")

    def end_mission(self):
        self.cancel_timer()
        final_grade = self.current_grade
        summary = self.result_summary()
        if self.current_user:
            self.store.delete_progress(self.current_user)
        self.store.log_result(self.player_name, self.current_grade, self.score)
        self.mount(ResultScreen, summary, lambda g=final_grade: self.start_new_mission(g))


if __name__ == "__main__":
    app = LiteracyMissionControl()
    app.mainloop()
