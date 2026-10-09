import random
import pygame
from game.text_box import TextBox
 
class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = ["PYTHON", "PYGAME", "PLANET", "ROCKET", "GALAXY", "STREAM", "PUZZLE", "ALGORITHM"]
        self.secret_word = ""
        self.scrambled_word = ""
        self.hint_count = 0

        self.score = 0
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        self.input_box = TextBox(width // 2 - 130, 210, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 + 45, 210, 95, 46)
        self.hint_btn = pygame.Rect(width // 2 + 150, 210, 95, 46)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)

        self.next_round()

    def scramble_string(self, word):
        letters = list(word)
        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)
            if shuffled != word or len(word) <= 1:
                return shuffled

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)
        self.hint_count = 0
        self.input_box.clear()

    def reveal_hint(self):
        if self.hint_count < len(self.secret_word):
            self.hint_count += 1
            self.score = max(0, self.score - 1)

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()
        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)
            self.next_round()
        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit_guess()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()
            elif self.hint_btn.collidepoint(event.pos):
                self.reveal_hint()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((26, 30, 38))

        title_surf = self.font_title.render("Word Scramble Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_msg.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 70))

        spaced_letters = "  ".join(self.scrambled_word)
        scramble_surf = self.font_word.render(spaced_letters, True, (100, 200, 255))
        screen.blit(scramble_surf, (self.width // 2 - scramble_surf.get_width() // 2, 130))

        hinted_word = " ".join(
            self.secret_word[index] if index < self.hint_count else "_"
            for index in range(len(self.secret_word))
        )
        hint_surf = self.font_msg.render(hinted_word, True, (210, 215, 225))
        screen.blit(hint_surf, (self.width // 2 - hint_surf.get_width() // 2, 178))

        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 85), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(btn_text, (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2))

        pygame.draw.rect(screen, (55, 105, 155), self.hint_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.hint_btn, width=2, border_radius=6)
        hint_btn_text = self.font_btn.render("HINT", True, (255, 255, 255))
        screen.blit(hint_btn_text, (self.hint_btn.centerx - hint_btn_text.get_width() // 2, self.hint_btn.centery - hint_btn_text.get_height() // 2))

        feedback_surf = self.font_msg.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 285))
