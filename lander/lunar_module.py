import time

import pyxel

from .utils import Sprite

CRASH_SPEED = 0.3
LAND_SPEED = 0.1
TRUSTER_FORCE = 0.6
FUEL = 100


class LunarModule:

    sprites = {
        'idle': [
            Sprite(0, 8, 0, 8, 8, 0),
        ],
        'lost':  [],
        'landed': [
            Sprite(0, 8, 0, 8, 8, 0),
        ],
        'crashed': [
            Sprite(0, 32, 0, 8, 8, 0),
            Sprite(0, 32, 8, 8, 8, 0),
        ],
        'damaged': [
            Sprite(0, 40, 0, 8, 8, 0),
            Sprite(0, 40, 8, 8, 8, 0),
        ],
        'bottom-thruster': [
            Sprite(0, 0, 8, 8, 8, 0),
            Sprite(0, 8, 8, 8, 8, 0),
        ],
        'left-thruster': [
            Sprite(0, 16, 0, 8, 8, 0),
            Sprite(0, 24, 0, 8, 8, 0),
        ],
        'right-thruster': [
            Sprite(0, 16, 8, 8, 8, 0),
            Sprite(0, 24, 8, 8, 8, 0),
        ],
    }

    flag = Sprite(0, 48, 0, 8, 8, 0)

    def __init__(self, x, y, gravity):
        self.x = x
        self.y = y
        self.action = 'idle'
        self.gravity = gravity
        self.velocity_x = 0
        self.velocity_y = 0
        self.fuel = FUEL
        self.last_time = time.time()

    def get_frame(self):
        frames = self.sprites[self.action]

        return frames[int(time.time() % len(frames))]

    def get_time_step(self):
        current_time = time.time()

        time_step = current_time - self.last_time

        self.last_time = current_time

        return time_step

    def check_collision(self, moon):
        for surface in moon.surface:
            y = int(self.y + 8 - surface.y)

            if y >= 0 and y < 16:
                left_x = int(self.x - surface.x)
                right_x = int(self.x + 8 - surface.x)

                if left_x >= 0 and left_x < 16:
                    collision_value = pyxel.image(surface.sprite.img).get(
                        surface.sprite.u + left_x,
                        surface.sprite.v + y,
                    )

                    return collision_value

                if right_x >= 0 and right_x < 16:
                    collision_value = pyxel.image(surface.sprite.img).get(
                        surface.sprite.u + right_x,
                        surface.sprite.v + y,
                    )

                    return collision_value

        return 0

    def update(self, moon):
        collision_value = self.check_collision(moon)

        if collision_value:
            if collision_value == 11:
                vx = self.velocity_x
                vy = self.velocity_y

                if vx < LAND_SPEED and vy < LAND_SPEED:
                    self.action = 'landed'
                elif vx < CRASH_SPEED and vy < CRASH_SPEED:
                    self.action = 'damaged'
                else:
                    self.action = 'crashed'
            else:
                self.action = 'crashed'
        else:
            thruster_x = 0
            thruster_y = 0

            if pyxel.btn(pyxel.KEY_DOWN) and self.fuel > 0:
                self.action = 'bottom-thruster'
                thruster_y = TRUSTER_FORCE
                self.fuel -= TRUSTER_FORCE
            elif pyxel.btn(pyxel.KEY_LEFT) and self.fuel > 0:
                self.action = 'left-thruster'
                thruster_x = TRUSTER_FORCE
                self.fuel -= TRUSTER_FORCE
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.fuel > 0:
                self.action = 'right-thruster'
                thruster_x = -TRUSTER_FORCE
                self.fuel -= TRUSTER_FORCE
            else:
                self.action = 'idle'

            time_step = self.get_time_step()

            self.velocity_x += thruster_x * time_step
            self.velocity_y += (self.gravity - thruster_y) * time_step

            self.x += self.velocity_x
            self.y += self.velocity_y

    def draw(self):
        frame = self.get_frame()

        pyxel.blt(
            self.x, self.y, frame.img, frame.u, frame.v, frame.w, frame.h,
            frame.colkey,
        )

        if self.action == 'landed':
            pyxel.blt(
                self.x + 8, self.y, self.flag.img, self.flag.u, self.flag.v,
                self.flag.w, self.flag.h, self.flag.colkey,
            )
