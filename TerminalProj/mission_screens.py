import os

import customtkinter as ctk


class BaseScreen(ctk.CTkFrame):
    def __init__(self, app, theme, **kwargs):
        super().__init__(app, fg_color="transparent", **kwargs)
        self.app = app
        self.theme = theme
        self.message_label = None

    def page_shell(self, panel_color=None):
        shell = ctk.CTkFrame(self, corner_radius=30, fg_color=panel_color or self.theme["panel"])
        shell.pack(fill="both", expand=True, padx=28, pady=28)
        return shell

    def page_title(self, parent, title, subtitle):
        block = ctk.CTkFrame(parent, fg_color="transparent")
        block.pack(fill="x", padx=34, pady=(30, 12))
        ctk.CTkLabel(block, text=title, font=("Orbitron", 34, "bold"), text_color=self.theme["highlight"]).pack()
        ctk.CTkLabel(block, text=subtitle, font=("Arial", 14), text_color=self.theme["muted"]).pack(pady=(6, 0))
        return block

    def status_message(self, parent):
        self.message_label = ctk.CTkLabel(parent, text="", font=("Arial", 13), text_color=self.theme["highlight"])
        return self.message_label

    def show_message(self, text, color=None):
        if self.message_label:
            self.message_label.configure(text=text, text_color=color or self.theme["highlight"])

    def glass_card(self, parent, color=None):
        return ctk.CTkFrame(parent, corner_radius=26, fg_color=color or self.theme["card"])

    def surface_card(self, parent, color, border=None, radius=26, padx=None, pady=None):
        card = ctk.CTkFrame(
            parent,
            corner_radius=radius,
            fg_color=color,
            border_width=1 if border else 0,
            border_color=border or color,
        )
        if padx is not None or pady is not None:
            card.pack(fill="x", padx=padx or 0, pady=pady or 0)
        return card

    def action_button(self, parent, text, command, fg=None, hover=None, text_color=None, width=None):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=44,
            width=width or 0,
            corner_radius=14,
            fg_color=fg or self.theme["highlight"],
            hover_color=hover or self.theme["highlight_hover"],
            text_color=text_color or self.theme["button_text"],
            font=("Arial", 14, "bold"),
        )
        return button

    def on_resize(self):
        return


class AuthScreen(BaseScreen):
    def __init__(self, app, theme):
        super().__init__(app, theme)
        self.mode = "login"
        shell = self.page_shell()
        self.content = ctk.CTkFrame(shell, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=26, pady=22)
        self.content.grid_columnconfigure(0, weight=2)
        self.content.grid_columnconfigure(1, weight=3)
        self.content.grid_rowconfigure(0, weight=1)

        self.hero = self.glass_card(self.content, self.theme["hero"])
        self.hero.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._build_hero(self.hero)

        self.form_panel = ctk.CTkFrame(self.content, corner_radius=26, fg_color="#f6fbf8")
        self.form_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self._build_form(self.form_panel)
        self.update_mode()

    def _build_hero(self, parent):
        self.hero_badge = ctk.CTkLabel(parent, text="LITERACY MISSION", font=("Arial", 12, "bold"), text_color=self.theme["light"])
        self.hero_badge.pack(anchor="w", padx=34, pady=(40, 18))

        self.hero_title = ctk.CTkLabel(parent, text="", font=("Orbitron", 42, "bold"), text_color=self.theme["light"])
        self.hero_title.pack(anchor="w", padx=34, pady=(10, 8))

        self.hero_text = ctk.CTkLabel(
            parent,
            text="",
            font=("Arial", 18),
            text_color=self.theme["muted"],
            wraplength=330,
            justify="left",
        )
        self.hero_text.pack(anchor="w", padx=34)

        self.hero_chips = ctk.CTkFrame(parent, fg_color="transparent")
        self.hero_chips.pack(anchor="w", padx=34, pady=(26, 0))
        for text in ["XP Tracking", "Saved Progress", "Fast Access"]:
            chip = ctk.CTkFrame(self.hero_chips, corner_radius=18, fg_color=self.theme["chip"])
            chip.pack(side="left", padx=(0, 10))
            ctk.CTkLabel(chip, text=text, font=("Arial", 12, "bold"), text_color=self.theme["light"]).pack(padx=14, pady=8)

        self.hero_switch = self.action_button(
            parent,
            "",
            self.toggle_mode,
            fg="transparent",
            hover=self.theme["chip"],
            text_color=self.theme["light"],
            width=160,
        )
        self.hero_switch.configure(border_width=1, border_color=self.theme["light"])
        self.hero_switch.pack(anchor="w", padx=34, pady=(34, 36))

    def _build_form(self, parent):
        self.form_title = ctk.CTkLabel(parent, text="", font=("Arial", 38, "bold"), text_color="#2db8a7")
        self.form_title.pack(pady=(42, 8))
        self.form_subtitle = ctk.CTkLabel(parent, text="", font=("Arial", 16), text_color="#7f8b8f")
        self.form_subtitle.pack()

        self.helper_text = ctk.CTkLabel(parent, text="", font=("Arial", 13), text_color="#a0a9ac")
        self.helper_text.pack(pady=(14, 18))

        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", padx=36, pady=(30, 0))

        self.username_entry = ctk.CTkEntry(
            form,
            height=54,
            corner_radius=12,
            border_width=0,
            fg_color="#edf3f1",
            text_color="#223033",
            font=("Arial", 16),
            placeholder_text="Username",
            placeholder_text_color="#7f8b8f"
        )
        self.username_entry.pack(fill="x")

        self.password_entry = ctk.CTkEntry(
            form,
            height=54,
            corner_radius=12,
            border_width=0,
            fg_color="#edf3f1",
            text_color="#223033",
            font=("Arial", 16),
            placeholder_text="Password",
            placeholder_text_color="#7f8b8f",
            show="*",
        )
        self.password_entry.pack(fill="x", pady=(16, 0))

        buttons = ctk.CTkFrame(parent, fg_color="transparent")
        buttons.pack(fill="x", padx=36, pady=(24, 0))
        self.primary_button = self.action_button(
            buttons,
            "",
            self.submit_mode,
            fg="#40b7ac",
            hover="#2da79b",
            text_color="white",
        )
        self.primary_button.pack(fill="x")

        self.switch_hint = ctk.CTkLabel(parent, text="", font=("Arial", 14), text_color="#7f8b8f")
        self.switch_hint.pack(pady=(16, 6))
        self.inline_switch = ctk.CTkButton(
            parent,
            text="",
            command=self.toggle_mode,
            fg_color="transparent",
            hover=False,
            text_color="#2db8a7",
            font=("Arial", 14, "bold"),
            height=28,
        )
        self.inline_switch.pack()

        self.status_message(parent).pack(pady=(16, 30))

    def update_mode(self):
        login_mode = self.mode == "login"
        self.hero_title.configure(text="Welcome Back!" if login_mode else "New Pilot?")
        self.hero_text.configure(
            text="Resume your literacy mission, load your saved progress, and keep earning XP."
            if login_mode
            else "Create your pilot account and get ready for a modern gamified reading mission."
        )
        self.hero_switch.configure(text="SIGN UP" if login_mode else "SIGN IN")

        self.form_title.configure(text="Sign In" if login_mode else "Create Account")
        self.form_subtitle.configure(text="Use username and password only.")
        self.helper_text.configure(
            text="Use an account created inside this literacy system."
            if login_mode
            else "Create a new account inside this literacy system."
        )
        self.username_entry.configure(placeholder_text="Username")
        self.password_entry.configure(placeholder_text="Password")
        self.primary_button.configure(text="SIGN IN" if login_mode else "SIGN UP")
        self.switch_hint.configure(
            text="Don't have an account yet?" if login_mode else "Already have an account?"
        )
        self.inline_switch.configure(text="Create one here" if login_mode else "Return to sign in")

    def toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.show_message("")
        self.update_mode()

    def submit_mode(self):
        if self.mode == "login":
            self.handle_login()
        else:
            self.handle_register()

    def handle_login(self):
        self.app.login_user(self.username_entry.get().strip(), self.password_entry.get().strip(), self)

    def handle_register(self):
        self.app.register_user(self.username_entry.get().strip(), self.password_entry.get().strip(), self)

    def on_resize(self):
        compact = self.app.winfo_width() < 980
        if compact:
            self.hero.grid_configure(row=0, column=0, padx=0, pady=(0, 12))
            self.form_panel.grid_configure(row=1, column=0, padx=0, pady=(12, 0))
            self.content.grid_columnconfigure(0, weight=1)
            self.content.grid_columnconfigure(1, weight=1)
            self.hero_title.configure(font=("Orbitron", 34, "bold"))
            self.hero_text.configure(wraplength=max(self.app.winfo_width() - 180, 260))
        else:
            self.hero.grid_configure(row=0, column=0, padx=(0, 10), pady=0)
            self.form_panel.grid_configure(row=0, column=1, padx=(10, 0), pady=0)
            self.content.grid_columnconfigure(0, weight=2)
            self.content.grid_columnconfigure(1, weight=3)
            self.hero_title.configure(font=("Orbitron", 42, "bold"))
            self.hero_text.configure(wraplength=330)


class MenuScreen(BaseScreen):
    def __init__(self, app, theme, username, progress):
        super().__init__(app, theme)
        self.app.set_background(self.theme.get("menu_bg"))
        shell = ctk.CTkFrame(self, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=20, pady=20)
        self.page_title(shell, "Mission Control", f"Welcome back, {username}")

        topbar = ctk.CTkFrame(shell, fg_color="transparent")
        topbar.pack(fill="x", padx=32, pady=(0, 12))
        self.status_message(topbar).pack(side="left")
        self.action_button(
            topbar,
            "Log Out",
            app.logout,
            fg=self.theme["menu_delete"],
            hover="#f25f5c",
            text_color="white",
            width=116,
        ).pack(side="right")

        content = ctk.CTkFrame(shell, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=26, pady=(8, 24))
        content.grid_columnconfigure((0, 1), weight=1, uniform="menu")
        content.grid_rowconfigure((0, 1), weight=1)

        grade_cards = [
            ("Grade 4", "Forest Sector", "4", self.theme["menu_card"], self.theme["forest_accent"]),
            ("Grade 5", "Volcano Zone", "5", self.theme["menu_card"], self.theme["volcano_accent"]),
            ("Grade 6", "Cyber City", "6", self.theme["menu_card"], self.theme["cyber_accent"]),
        ]
        for idx, (title, subtitle, grade, color, accent) in enumerate(grade_cards):
            card = self._menu_card(content, idx, color)
            ctk.CTkLabel(card, text=title, font=("Arial", 26, "bold"), text_color=self.theme["light"]).pack(anchor="w", padx=28, pady=(26, 6))
            ctk.CTkLabel(card, text=subtitle, font=("Arial", 14), text_color=accent).pack(anchor="w", padx=28)
            ctk.CTkLabel(
                card,
                text="Fresh mission with shuffled stories and clean progress tracking.",
                font=("Arial", 13),
                text_color=self.theme["muted"],
                wraplength=340,
                justify="left",
            ).pack(anchor="w", padx=28, pady=(14, 20))
            self.action_button(
                card,
                "Start New Mission",
                lambda g=grade: app.start_new_mission(g),
                fg=self.theme["menu_button"],
                hover=self.theme["menu_button"],
                text_color=self.theme["menu_button_text"],
            ).pack(fill="x", padx=28, pady=(0, 24))

        progress_card = self._menu_card(content, 3, self.theme["menu_progress"])
        ctk.CTkLabel(progress_card, text="Saved Progress", font=("Arial", 26, "bold"), text_color=self.theme["light"]).pack(anchor="w", padx=28, pady=(26, 6))
        summary = "No saved progress yet."
        if progress:
            summary = (
                f"Grade {progress['grade']}  |  Story {progress['story_idx'] + 1}/10\n"
                f"Question {progress['q_idx'] + 1}  |  Score {progress['score']}  |  Rank {progress['rank']}"
            )
        ctk.CTkLabel(progress_card, text=summary, font=("Arial", 13), text_color=self.theme["muted"], justify="left").pack(anchor="w", padx=28, pady=(10, 20))
        self.action_button(progress_card, "Load Progress", app.load_progress, fg=self.theme["menu_button"], hover=self.theme["menu_button"], text_color=self.theme["menu_button_text"]).pack(fill="x", padx=28, pady=(0, 10))
        self.action_button(progress_card, "Delete Save", app.delete_save_from_menu, fg=self.theme["menu_delete"], hover="#f25f5c", text_color="white").pack(fill="x", padx=28, pady=(0, 24))

    def _menu_card(self, parent, index, color):
        row, column = divmod(index, 2)
        card = ctk.CTkFrame(parent, corner_radius=28, fg_color=color, border_width=1, border_color=self.theme["soft_line"])
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        return card


class MissionScreen(BaseScreen):
    def __init__(self, app, theme, state, story, question_text, answer):
        super().__init__(app, theme)
        self.answer = answer
        self.layout_mode = None
        self.review_overlay = None

        self.app.set_background(theme["bg_image"])

        shell = ctk.CTkFrame(self, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=14, pady=14)
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(1, weight=1)

        self._build_hud(shell, state)
        self._build_story_area(shell, state, story)
        self._build_question_area(shell, question_text)
        self.on_resize()

    def _build_hud(self, parent, state):
        hud_shadow = ctk.CTkFrame(parent, fg_color="transparent")
        hud_shadow.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hud = self.surface_card(hud_shadow, self.theme["hud_color"], self.theme["panel_edge"], radius=24)
        hud.pack(fill="x")
        hud.grid_columnconfigure(0, weight=3)
        hud.grid_columnconfigure(1, weight=2)
        hud.grid_columnconfigure(2, weight=3)
        hud.grid_columnconfigure(3, weight=1)

        left = ctk.CTkFrame(hud, fg_color="transparent")
        left.grid(row=0, column=0, sticky="ew", padx=(18, 10), pady=16)
        ctk.CTkLabel(left, text=f"PILOT  {state['player_name']}", font=("Orbitron", 17, "bold"), text_color=self.theme["accent"]).pack(anchor="w")
        self.xp_bar = ctk.CTkProgressBar(left, height=12, corner_radius=10, progress_color=self.theme["accent"], fg_color=self.theme["question_glow"])
        self.xp_bar.set(state["xp"] % 1000 / 1000)
        self.xp_bar.pack(fill="x", pady=(10, 0))

        self.rank_label = ctk.CTkLabel(hud, text=f"Rank: {state['rank']}", font=("Arial", 16, "bold"), text_color=self.theme["light"])
        self.rank_label.grid(row=0, column=1, sticky="w", padx=10, pady=16)

        actions = ctk.CTkFrame(hud, fg_color="transparent")
        actions.grid(row=0, column=2, sticky="e", padx=10, pady=16)
        self.action_button(actions, "Save", app_command(self.app.handle_save_and_menu), fg=self.theme["highlight"], hover=self.theme["highlight_hover"]).pack(side="left", padx=6)
        self.action_button(actions, "Pause", app_command(self.app.pause_quiz), fg=self.theme["secondary"], hover=self.theme["secondary_hover"], text_color=self.theme["secondary_text"]).pack(side="left", padx=6)
        self.action_button(actions, "Stop", app_command(self.app.end_mission), fg="#ff7a7a", hover="#f25f5c", text_color="white").pack(side="left", padx=6)

        timer_card = self.surface_card(hud, self.theme["question_glow"], self.theme["soft_line"], radius=18)
        timer_card.grid(row=0, column=3, sticky="e", padx=(10, 18), pady=16)
        self.timer_label = ctk.CTkLabel(timer_card, text=f"{state['timer_seconds']}s", font=("Orbitron", 18, "bold"), text_color="#ffd166")
        self.timer_label.pack(padx=18, pady=10)

    def _build_story_area(self, parent, state, story_text):
        self.content = ctk.CTkFrame(parent, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_columnconfigure(2, weight=0)
        self.content.grid_rowconfigure((0, 1), weight=1)

        self.story_card = ctk.CTkFrame(self.content, corner_radius=28, fg_color="transparent", border_width=1, border_color=self.theme["panel_edge"], width=340)
        self.story_card.grid(row=0, column=0, sticky="nsw", padx=(0, 18), pady=(0, 14))
        self.story_card.grid_propagate(False)
        ctk.CTkLabel(
            self.story_card,
            text=f"SITUATION REPORT {state['story_idx'] + 1}/10",
            font=("Arial", 13, "bold"),
            text_color=self.theme["accent"],
        ).pack(anchor="w", padx=24, pady=(20, 8))
        self.story_box = ctk.CTkTextbox(
            self.story_card,
            font=("Georgia", 18),
            fg_color=self.theme["input_fill"],
            text_color=self.theme["light"],
            corner_radius=16,
            border_width=0,
            wrap="word",
        )
        self.story_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.story_box.insert("0.0", story_text)
        self.story_box.configure(state="disabled")

        self.preview_card = ctk.CTkFrame(self.content, corner_radius=28, fg_color="transparent")
        self.preview_card.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=(0, 14))
        inner = self.surface_card(self.preview_card, self.theme["overlay"], self.theme["soft_line"], radius=28)
        inner.pack(fill="both", expand=True, padx=8, pady=8)
        self.story_preview = ctk.CTkLabel(
            inner,
            text=story_text,
            font=("Georgia", 21, "bold"),
            text_color=self.theme["hero_text"],
            justify="left",
            anchor="nw",
        )
        self.story_preview.pack(fill="both", expand=True, padx=30, pady=28)

    def _build_question_area(self, parent, question_text):
        shell = ctk.CTkFrame(parent, fg_color="transparent")
        shell.grid(row=2, column=0, sticky="ew")
        body = self.surface_card(shell, self.theme["hud_color"], self.theme["panel_edge"], radius=26)
        body.pack(fill="x", padx=18, pady=(8, 0))
        body.grid_columnconfigure(0, weight=1)

        self.question_label = ctk.CTkLabel(body, text=question_text, font=("Arial", 26, "bold"), text_color=self.theme["light"], justify="center")
        self.question_label.grid(row=0, column=0, padx=24, pady=(22, 14), sticky="ew")
        self.answer_entry = ctk.CTkEntry(
            body,
            height=50,
            corner_radius=16,
            border_width=0,
            fg_color=self.theme["input_fill"],
            text_color=self.theme["light"],
            placeholder_text="Type your answer here...",
            placeholder_text_color=self.theme["muted"],
        )
        self.answer_entry.grid(row=1, column=0, padx=24, sticky="ew")
        self.answer_entry.focus_set()

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.grid(row=2, column=0, pady=16)
        self.action_button(actions, "Previous", self.app.show_previous_question, fg=self.theme["card_color"], hover=self.theme["question_glow"], text_color=self.theme["light"]).pack(side="left", padx=8)
        self.action_button(actions, "Submit Analysis", lambda: self.app.process_answer(self.answer)).pack(side="left", padx=8)
        self.action_button(actions, "Skip", self.app.skip_question, fg="#ffd166", hover="#ffca3a", text_color="#403100").pack(side="left", padx=8)

        self.feedback_label = ctk.CTkLabel(body, text="", font=("Arial", 14, "italic"), text_color=self.theme["muted"])
        self.feedback_label.grid(row=3, column=0, padx=24, pady=(0, 18), sticky="ew")

    def set_feedback(self, text, color):
        self.feedback_label.configure(text=text, text_color=color)

    def update_rank(self, xp, rank):
        self.xp_bar.set(xp % 1000 / 1000)
        self.rank_label.configure(text=f"Rank: {rank}")

    def update_timer(self, seconds):
        self.timer_label.configure(text=f"{seconds}s")

    def show_previous_review(self, snapshot):
        self.close_previous_review()
        self.review_overlay = ctk.CTkFrame(self, fg_color="#000000")
        self.review_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = self.surface_card(self.review_overlay, self.theme["panel"], self.theme["panel_edge"], radius=28)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Previous Question", font=("Orbitron", 28, "bold"), text_color=self.theme["highlight"]).pack(anchor="w", padx=28, pady=(24, 10))
        ctk.CTkLabel(card, text=snapshot["question"], font=("Arial", 20, "bold"), text_color=self.theme["light"], wraplength=700, justify="left").pack(anchor="w", padx=28)

        story_box = ctk.CTkTextbox(card, width=760, height=170, corner_radius=18, border_width=0, fg_color=self.theme["input_fill"], text_color=self.theme["light"], wrap="word", font=("Georgia", 16))
        story_box.pack(padx=28, pady=(18, 14), fill="both")
        story_box.insert("0.0", snapshot["story"])
        story_box.configure(state="disabled")

        meta = ctk.CTkFrame(card, fg_color="transparent")
        meta.pack(fill="x", padx=28, pady=(0, 12))
        for label, value, color in [
            ("Your Answer", snapshot["user_answer"] or "No answer", self.theme["light"]),
            ("Accepted", snapshot["accepted"], self.theme["accent"]),
            ("Result", snapshot["result"], snapshot["result_color"]),
        ]:
            block = self.surface_card(meta, self.theme["overlay"], self.theme["soft_line"], radius=18)
            block.pack(fill="x", pady=6)
            ctk.CTkLabel(block, text=label, font=("Arial", 12, "bold"), text_color=self.theme["muted"]).pack(anchor="w", padx=16, pady=(12, 4))
            ctk.CTkLabel(block, text=value, font=("Arial", 15, "bold"), text_color=color, wraplength=680, justify="left").pack(anchor="w", padx=16, pady=(0, 12))

        self.action_button(card, "Close Review", self.app.close_previous_question).pack(fill="x", padx=28, pady=(6, 24))

    def close_previous_review(self):
        if self.review_overlay:
            self.review_overlay.destroy()
            self.review_overlay = None

    def on_resize(self):
        compact = self.app.winfo_width() < 1120
        if compact and self.layout_mode != "compact":
            self.layout_mode = "compact"
            self.story_card.grid_configure(row=0, column=0, padx=0, pady=(0, 14), sticky="ew")
            self.preview_card.grid_configure(row=1, column=0, padx=0, pady=(0, 14), sticky="nsew")
            self.content.grid_columnconfigure(0, weight=1)
            self.content.grid_columnconfigure(1, weight=1)
            self.story_preview.configure(font=("Georgia", 19, "bold"))
            self.story_card.configure(width=0)
            self.story_card.grid_propagate(True)
        elif not compact and self.layout_mode != "wide":
            self.layout_mode = "wide"
            self.story_card.grid_configure(row=0, column=0, padx=(0, 18), pady=(0, 14), sticky="nsw")
            self.preview_card.grid_configure(row=0, column=1, padx=(0, 0), pady=(0, 14), sticky="nsew")
            self.content.grid_columnconfigure(0, weight=0)
            self.content.grid_columnconfigure(1, weight=1)
            self.story_preview.configure(font=("Georgia", 21, "bold"))
            self.story_card.configure(width=340)
            self.story_card.grid_propagate(False)

        wrap = max(self.app.winfo_width() - 140, 320)
        self.question_label.configure(wraplength=wrap)
        self.feedback_label.configure(wraplength=wrap)
        self.story_preview.configure(wraplength=max(int(self.app.winfo_width() * 0.5), 360))


class ResultScreen(BaseScreen):
    def __init__(self, app, theme, summary, replay_command):
        super().__init__(app, theme)
        shell = ctk.CTkFrame(self, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=20, pady=20)
        shell.grid_columnconfigure((0, 1), weight=1, uniform="result")
        shell.grid_rowconfigure(0, weight=1)

        hero = ctk.CTkFrame(
            shell,
            corner_radius=32,
            fg_color=self.theme["hero"],
            border_width=1,
            border_color=self.theme["soft_line"],
        )
        hero.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ctk.CTkLabel(hero, text="MISSION COMPLETE", font=("Orbitron", 16, "bold"), text_color=self.theme["accent"]).pack(anchor="w", padx=36, pady=(40, 18))
        ctk.CTkLabel(hero, text="Great run, pilot.", font=("Orbitron", 38, "bold"), text_color=self.theme["light"]).pack(anchor="w", padx=36)
        ctk.CTkLabel(
            hero,
            text="Your literacy mission is logged, your rank is updated, and you can head back to mission control for another round.",
            font=("Arial", 17),
            text_color=self.theme["muted"],
            wraplength=420,
            justify="left",
        ).pack(anchor="w", padx=36, pady=(16, 0))

        chip_row = ctk.CTkFrame(hero, fg_color="transparent")
        chip_row.pack(anchor="w", padx=36, pady=(28, 0))
        for text in ["Progress Recorded", "Rank Updated", "Ready For Next Mission"]:
            chip = ctk.CTkFrame(chip_row, corner_radius=18, fg_color=self.theme["chip"])
            chip.pack(side="left", padx=(0, 10))
            ctk.CTkLabel(chip, text=text, font=("Arial", 12, "bold"), text_color=self.theme["light"]).pack(padx=14, pady=8)

        stats = ctk.CTkFrame(
            shell,
            corner_radius=32,
            fg_color=self.theme["overlay"],
            border_width=1,
            border_color=self.theme["panel_edge"],
        )
        stats.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        ctk.CTkLabel(stats, text="Mission Summary", font=("Arial", 28, "bold"), text_color=self.theme["light"]).pack(pady=(42, 24))

        self._result_stat(stats, "Final Score", f"{summary['score']}/{summary['total_questions']}", self.theme["highlight"])
        self._result_stat(stats, "Correct Answers", str(summary["score"]), "#7cf29a")
        self._result_stat(stats, "XP Earned", f"+{summary['xp_earned']}", self.theme["accent"])
        self._result_stat(stats, "Mission Grade", summary["mission_grade"], "#ffd166")
        self._result_stat(stats, "Rank Achieved", summary["rank"], "#ffd166")

        self.action_button(
            stats,
            "Return To Base",
            app.show_main_menu,
            fg=self.theme["highlight"],
            hover=self.theme["highlight_hover"],
            text_color=self.theme["button_text"],
        ).pack(fill="x", padx=46, pady=(32, 12))

        self.action_button(
            stats,
            "Play Another Mission",
            replay_command,
            fg=self.theme["secondary"],
            hover=self.theme["secondary_hover"],
            text_color=self.theme["secondary_text"],
        ).pack(fill="x", padx=46, pady=(0, 34))

    def _result_stat(self, parent, label, value, color):
        card = ctk.CTkFrame(
            parent,
            corner_radius=22,
            fg_color=self.theme["card"],
            border_width=1,
            border_color=self.theme["soft_line"],
        )
        card.pack(fill="x", padx=34, pady=10)
        ctk.CTkLabel(card, text=label, font=("Arial", 13, "bold"), text_color=self.theme["muted"]).pack(anchor="w", padx=22, pady=(18, 6))
        ctk.CTkLabel(card, text=value, font=("Orbitron", 28, "bold"), text_color=color).pack(anchor="w", padx=22, pady=(0, 18))

    def on_resize(self):
        return


def app_command(command):
    return command
