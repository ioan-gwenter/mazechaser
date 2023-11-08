import tkinter

from map import *


class RayCast:
    """
    Data Structure for handling casting of rays, and rendering the display of the game.
    """

    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.canvas = game.mini_map.map_display

        self.sky_height = 0
        self.sky_image = PhotoImage(file="assets/sky.png")
        self.hands = PhotoImage(file="assets/hands.png")
        self.boss_image = PhotoImage(file="assets/boss_key.png")

    def render_background(self):
        self.game.display.create_image(0, 0, image=self.sky_image, anchor=tkinter.NW)
        self.game.display.create_rectangle(0, self.sky_height, RES_WIDTH, RES_HEIGHT, fill="#504C4B")

    def render_hands(self):
        self.game.display.create_image(0, 0, image=self.hands, anchor=tkinter.NW)

    def render_timer(self):
        self.game.display.create_text(900, 50,
                                      text=self.game.timer.get_time(),
                                      fill="black",
                                      font='Helvetica 40 bold')

    def render_boss(self):
        self.game.display.create_image(0, 0, image=self.boss_image, anchor=tkinter.NW)

    def ray_cast(self):
        """
        Method Casts all rays from the players coordinate based on their FOV and angle.
        Then renders their view onto the Game Classes display.
        - algorithm is based on a fast DDA implementation
        """

        # Getting the coordinate of the player, and their cell.
        # Gets the starting angle of the players FOV

        self.render_background()
        start_x, start_y = self.player.get_pos()
        map_x, map_y = self.player.get_map_pos()
        ray_angle = self.player.player_angle - (FOV / 2) + 0.0000001
        longest_dist = 0

        # Calculate Ray Depth and Intersect using FAST DDA algorithm

        for ray in range(RAY_NUM):

            # Players current angle
            sin = m.sin(ray_angle)
            cos = m.cos(ray_angle)

            # Array stores how many units to step along each grid axis
            ray_step = [0, 0]
            ray_length = [0, 0]

            # map_check holds the cell being currently observed.
            # intersect holds the canvas coordinate of any intersection with the ray and walls
            map_check = [map_x, map_y]
            intersect = [0, 0]

            tile_found = False
            max_dist = 1000
            dist = 0.0
            is_end = False

            # Check if Negative X Direction
            if cos < 0:
                ray_step[0] = -1
                unit_x = -cos
                ray_length[0] = (start_x - float((map_x - 0.0001) * BLOCK_SIZE)) / unit_x

            # Else it is Positive X Direction
            else:
                ray_step[0] = 1
                unit_x = cos
                ray_length[0] = (float((map_x + 1) * BLOCK_SIZE) - start_x) / unit_x

            # Check Negative Y Direction
            if sin < 0:
                ray_step[1] = -1
                unit_y = -sin
                ray_length[1] = (start_y - float((map_y - 0.00001) * BLOCK_SIZE)) / unit_y

            # Else it is Positive Y Direction
            else:
                ray_step[1] = 1
                unit_y = sin
                ray_length[1] = (float((map_y + 1) * BLOCK_SIZE) - start_y) / unit_y

            # While the tile the intersect occurs in has not been found, and maximum ray depth not reached
            while not tile_found and dist < max_dist:

                # if the distance of dx < dy
                if ray_length[0] < ray_length[1]:
                    map_check[0] += ray_step[0]
                    dist = ray_length[0]
                    ray_length[0] += BLOCK_SIZE / unit_x

                # else if dx > dy
                else:
                    map_check[1] += ray_step[1]
                    dist = ray_length[1]
                    ray_length[1] += BLOCK_SIZE / unit_y

                # Check if target tile is in game map
                if 0 <= map_check[0] < game_map_width and map_check[1] >= 0 and map_check[
                    1] < game_map_height:
                    if (map_check[0], map_check[1]) in self.game.mini_map.world_map:
                        if self.game.mini_map.world_map[map_check[0], map_check[1]] == 1 or 3:
                            if self.game.mini_map.world_map[map_check[0], map_check[1]] == 3:
                                is_end = True
                            tile_found = True

            # Drawing Rays onto the map
            if tile_found:
                intersect = [start_x + (cos * dist), start_y + (sin * dist)]
                if self.game.dev_mode:
                    self.canvas.create_line(self.player.player_x, self.player.player_y, intersect[0],
                                            intersect[1])

            # Fish Bowl Removal
            # Multiplies by cos of the perspective of the player to remove curvature (using Range not dist)
            # http://www.playfuljs.com/a-first-person-engine-in-265-lines/ to see more
            dist *= m.cos(self.player.player_angle - ray_angle)

            # Rendering Walls in game.
            # Height is scaled by the distance the player is to the intersect
            height = SCREEN_DISTANCE / ((dist / 20) + 0.0001)

            # Calculates sky height
            if dist > longest_dist:
                longest_dist = dist
                self.sky_height = (HALF_RES_HEIGHT / 2) + (height - 10)

            color_dist = int(dist)
            # Colours cannot exceed 255, so max colour / 2 = (255*2)
            if color_dist > 510:
                color_dist = 510

            darkness_mod = (510 - color_dist) / 510
            ns_mod_x, ns_mod_y = self.game.player.get_pos()
            ns_mod = 1
            ns_mod = ns_mod_x / (maze.maze_x*100)
            # Colour Handling
            color = 245, 226, 61
            r = 255
            b = 255
            g = 1
            rgb_color = (int(darkness_mod * r * ns_mod), int(darkness_mod * g * (1-ns_mod)), int(darkness_mod * b))
            if is_end:
                r = 31
                g = 250
                b = 20
                rgb_color = (int(darkness_mod * r), int(darkness_mod * g), int(darkness_mod * b))

            # Convert the RGB value to hex string for tkinter format
            hex_color = '#%02x%02x%02x' % rgb_color

            # Sets corners of cells to black to identify individual cells in game
            if int(intersect[0]) % 100 == 0 and int(intersect[1]) % 100 == 0 or int(
                    intersect[0] + 1) % 100 == 0 and int(intersect[1] + 1) % 100 == 0:
                hex_color = "#000000"

            # Draws the wall segment onto the screen
            self.game.display.create_line(ray * SCALE, (HALF_RES_HEIGHT / 2) + height, ray * SCALE,
                                          (HALF_RES_HEIGHT / 2) - height, width=int(SCALE), fill=hex_color)
            ray_angle += DELTA_ANGLE

    def update(self):
        """
        Calls the raycast method
        """
        self.ray_cast()
        self.render_timer()
        self.render_hands()
        if self.game.boss_key:
            self.render_boss()
