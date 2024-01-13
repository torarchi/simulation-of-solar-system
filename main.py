import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция")

WHITE = (255, 255, 255)
BLUE = (100, 150, 237)
RED = (190, 40, 50)
DARK_GREY = (80, 75, 80)

FONT = pygame.font.SysFont('arial', 12)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU  # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, name, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass

        self.selected = False

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if self.selected:
            pygame.draw.circle(win, (255, 255, 0), (x, y), self.radius + 5, width=2)

        if len(self.orbit) >= 2:
            updated_points = []

            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def draw_3d_representation(self, planets):
        if self.selected:
            win_3d = pygame.display.set_mode((800, 800))
            pygame.display.set_caption("3D Representation")
            run_3d = True

            while run_3d:
                win_3d.fill((0, 0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_3d = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                        run_3d = False

                scaling_factor = 200 / self.AU * self.SCALE

                x_proj = int(self.x * scaling_factor + 400)
                y_proj = int(self.y * scaling_factor + 400)

                pygame.draw.circle(win_3d, (0, 255, 0), (x_proj, y_proj), self.radius + 5, width=2)

                info_text = FONT.render(f"Planet: {self.name} Distance: {round(self.distance_to_sun/1000, 1)} km", 1, WHITE)
                win_3d.blit(info_text, (400 - info_text.get_width() / 2, 780))

                for planet in planets:
                    if planet == self:
                        continue
                    dx = planet.x - self.x
                    dy = planet.y - self.y
                    x_other = int(planet.x * scaling_factor + 400)
                    y_other = int(planet.y * scaling_factor + 400)
                    pygame.draw.line(win_3d, (255, 255, 255), (x_proj, y_proj), (x_other, y_other), width=1)

                pygame.display.flip()

            pygame.display.set_mode((WIDTH, HEIGHT))



def main():
    run = True
    in_3d_representation = False
    clock = pygame.time.Clock()


    scale_factor = 1.0

    sun = Planet("Sun", 0, 0, 30, WHITE, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 16, BLUE, 5.9842 * 10 **24)
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet("Jupiter", -5.203 * Planet.AU, 0, 20, (255, 200, 100), 1.898e27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet("Saturn", -9.582 * Planet.AU, 0, 18, (210, 180, 140), 5.683e26)
    saturn.y_vel = 9.69 * 1000

    uranus = Planet("Uranus", -19.22 * Planet.AU, 0, 16, (173, 216, 230), 8.681e25)
    uranus.y_vel = 6.80 * 1000

    neptune = Planet("Neptune", -30.05 * Planet.AU, 0, 16, (70, 130, 180), 1.024e26)
    neptune.y_vel = 5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    scale_factor *= 1.1
                elif event.key == pygame.K_MINUS:
                    scale_factor /= 1.1
                elif event.key == pygame.K_9 and in_3d_representation:
                    in_3d_representation = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for planet in planets:
                        x = planet.x * planet.SCALE + WIDTH / 2
                        y = planet.y * planet.SCALE + HEIGHT / 2
                        distance = math.sqrt((event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2)

                        if distance <= planet.radius:
                            planet.selected = not planet.selected
                            if planet.selected:
                                planet.draw_3d_representation(planets)

        for planet in planets:
            planet.SCALE = 200 / Planet.AU * scale_factor
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
