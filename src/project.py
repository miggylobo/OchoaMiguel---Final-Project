import pygame
import random
from pygame import mixer

mixer.init()

image1 = pygame.image.load('cat1.png')
image2 = pygame.image.load('cat2.png')
image3 = pygame.image.load('cat3.png')
image4 = pygame.image.load('cat4.png')
image5 = pygame.image.load('cat5.png')
meow_sounds = [
    pygame.mixer.Sound('meow1.wav'),
    pygame.mixer.Sound('meow2.wav'),
    pygame.mixer.Sound('meow3.wav')
]


class Particle():

    def __init__(self, pos=(0, 0), size=15, life=10, image=None):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.age = 0 # in milliseconds
        self.life = life # in milliseconds
        self.dead = False
        self.alpha = 255
        self.shape = random.randrange(1, 6)
        self.surface = self.update_surface()
        
    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            # print("Particle is dead")
            self.dead = True
        self.alpha = 255 * (1 - self.age / self.life)

    def update_surface(self):
        surf = pygame.Surface((self.size * 1, self.size * 1), pygame.SRCALPHA)

        images = [image1, image2, image3, image4, image5]
        if 1 <= self.shape <= 5:
            image = images[self.shape - 1]
        else:
            image = None

        if image:
            image = pygame.transform.scale(image, (int(self.size * 1), int(self.size * 1)))
            surf.blit(image, (0, 0))
        
        return surf
    
    def draw(self, surface):
        if self.dead:
            # print("Skip drawing dead particles")
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)

class ParticleTrail():

    def __init__(self, pos, size, life):
        self.pos = pos
        self.size = size
        self.life = life
        self.particles = []

    def update(self, dt, direction_down=True):
        particle = Particle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle)
        self._update_particles(dt)
        self._update_pos(direction_down)

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]

    def _update_pos(self, direction_down):
        x, y = self.pos
        if direction_down == True:
            y += self.size
        elif direction_down == False:
            y -= self.size
        self.pos = (x, y)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Rain():

    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 15
        self.birth_rate = 1 # trails per frame
        self.trails = []
        self.direction_down = True

    def update(self, dt):
        self._birth_new_trails()
        self._update_trails(dt)
            
    
    def _update_trails(self, dt):
        for idx, trail in enumerate(self.trails):
            trail.update(dt, direction_down = self.direction_down)
            if self._trail_is_offscreen(trail):
                del self.trails[idx]

    def _trail_is_offscreen(self, trail):
        if self.direction_down == True:
            return trail.particles[-1].pos[1] > self.screen_res[1]
        elif self.direction_down == False:
            return trail.particles[-1].pos[1] < 0

    def _birth_new_trails(self):
        for count in range(self.birth_rate):
            screen_width = self.screen_res[0]
            x = random.randrange(0, screen_width, self.particle_size) 
            if self.direction_down == True:
                pos = (x, 0)
            elif self.direction_down == False:
                pos = (x, self.screen_res[1])
            life = random.randrange(500, 1000)
            trail = ParticleTrail(pos, self.particle_size, life)
            self.trails.insert(0, trail)

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Cat Rain!")
    clock = pygame.time.Clock()
    dt = 0
    possible_resolutions = [(1920, 1080), (960, 540), (480, 270)]
    current_resolution = 0
    screen = pygame.display.set_mode(possible_resolutions[current_resolution])
    rain = Rain(possible_resolutions[current_resolution])
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if rain.direction_down == True:
                        rain.direction_down = False
                    elif rain.direction_down == False:
                        rain.direction_down = True
                if pygame.mouse.get_pressed()[1]:
                    current_resolution = (current_resolution + 1) % len(possible_resolutions)
                    new_resolution = possible_resolutions[current_resolution]
                    screen = pygame.display.set_mode(new_resolution)
                    rain = Rain(new_resolution)
                if pygame.mouse.get_pressed()[2]:
                    mouse_pos = pygame.mouse.get_pos()
                    life = random.randrange(500, 1000)
                    trail = ParticleTrail(mouse_pos, rain.particle_size, life)
                    rain.trails.append(trail)
                    random.choice(meow_sounds).play()

        # TODO: some game logic
        rain.update(dt)
        # Render & Display
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        rain.draw(screen)
        pygame.display.flip()
        dt = clock.tick(12)
    pygame.quit()


if __name__ == "__main__":
    main()