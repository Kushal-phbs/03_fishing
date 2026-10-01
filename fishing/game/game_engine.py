"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.
"""

import pygame

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_DURATION_MS = 30_000


class GameEngine:
    def __init__(self):
        self.hook = Hook(
            x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5
        )
        self.fish_list = self._create_fish_list()
        self.hooked_fish = None
        self.hooked_fish_start_y = None
        self.score = 0
        self.game_over = False
        self.round_start_ticks = pygame.time.get_ticks()
        self.time_remaining = ROUND_DURATION_MS // 1000

    def _create_fish_list(self):
        return [
            Fish(x=100, y=180, speed=2, point_value=10, color=(80, 180, 220)),
            Fish(
                x=400,
                y=280,
                speed=-3,
                width=28,
                height=14,
                point_value=5,
                color=(110, 210, 120),
            ),
            Fish(
                x=250,
                y=380,
                speed=1,
                width=48,
                height=24,
                point_value=25,
                color=(245, 165, 60),
            ),
        ]

    def _update_timer(self):
        elapsed_ms = pygame.time.get_ticks() - self.round_start_ticks
        remaining_ms = max(0, ROUND_DURATION_MS - elapsed_ms)
        self.time_remaining = (remaining_ms + 999) // 1000
        if remaining_ms == 0:
            self.game_over = True

    def start_new_round(self):
        self._update_timer()
        if not self.game_over:
            return

        self.fish_list = self._create_fish_list()
        self.score = 0
        self.game_over = False
        self.round_start_ticks = pygame.time.get_ticks()
        self.time_remaining = ROUND_DURATION_MS // 1000
        self.hook.state = IDLE
        self.hook.y = self.hook.surface_y
        self.hooked_fish = None
        self.hooked_fish_start_y = None

    def start_cast(self):
        self._update_timer()
        if (
            not self.game_over
            and self.hook.state == IDLE
            and self.hook.y == self.hook.surface_y
        ):
            self.hook.start_cast()

    def update(self):
        self._update_timer()
        if self.game_over:
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                caught_fish = self.hooked_fish
                self.score += caught_fish.point_value
                caught_fish.y = self.hooked_fish_start_y
                if caught_fish.speed > 0:
                    caught_fish.x = -caught_fish.width / 2
                else:
                    caught_fish.x = WIDTH + caught_fish.width / 2
                self.fish_list.append(caught_fish)
                self.hooked_fish = None
                self.hooked_fish_start_y = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish_start_y = caught.y
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer

        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(
            surface, font, f"Time: {self.time_remaining}s", (WIDTH - 140, 10)
        )
        if self.game_over:
            renderer.draw_banner(
                surface, font, f"Final score: {self.score}    R: Restart"
            )
