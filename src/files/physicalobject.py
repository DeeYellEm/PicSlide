import pyglet
from . import util
import numpy as np
from itertools import combinations

class PhysicalObject(pyglet.sprite.Sprite):
    """A sprite with physical properties such as velocity"""

    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        # Location and Velocity
        self.x, self.y, self.vx, self.vy = 0,0,0,0

        # Radius and the r and v vectors required for the collision math
        self.radius = 1
        self.r = np.array((self.x, self.y))
        self.v = np.array((self.vx, self.vy))

        # Flag to remove this object from the game_object list
        self.dead = False

        # List of new objects to go in the game_objects list
        self.new_objects = []

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers = []


    # print([thing])
    def __repr__(self):
        return "PysicalObject.__repr__ x:% s y:% s vx:% s vy:% s radius:% s r:% s v:% s" % (self.x, self.y, self.vx, self.vy, self.radius, self.r, self.v)

    def overlaps(self, other):
        """Does the circle of this PysicalObject overlap that of other?"""

        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def update(self, dt):
        """This method should be called every frame."""

        # Update position according to velocity and time
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.r = np.array((self.x, self.y))
        self.v = np.array((self.vx, self.vy))

        # Wrap around the screen if necessary
        #self.check_bounds_wrap()
        self.check_bounds_wrap()

    def check_bounds_wrap(self):
        """Wrap around the edges"""
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        if self.y < min_y:
            self.y = max_y
        if self.x > max_x:
            self.x = min_x
        if self.y > max_y:
            self.y = min_y

    def check_bounds_bounce(self):
        """Bounce off the edges"""
        min_x = self.image.width/2
        min_y = self.image.height/2
        max_x = 800 - self.image.width/2
        max_y = 600 - self.image.height/2
        if self.x < min_x:
            self.x = min_x
            self.vx = -1*self.vx
        if self.x > max_x:
            self.x = max_x
            self.vx = -1*self.vx
        if self.y < min_y:
            self.y = min_y
            self.vy = -1*self.vy
        if self.y > max_y:
            self.y = max_y
            self.vy = -1*self.vy

    def collides_with(self, other_object):
        """Determine if this object collides with another"""

        # Ignore bullet collisions if we're supposed to
        # if not self.reacts_to_bullets and other_object.is_bullet:
        #     return False
        # if self.is_bullet and not other_object.reacts_to_bullets:
        #     return False

        # Calculate distance between object centers that would be a collision,
        # assuming square resources
        collision_distance = self.image.width * 0.5 * self.scale \
                             + other_object.image.width * 0.5 * other_object.scale

        # Get distance using position tuples
        actual_distance = util.distance(self.position, other_object.position)

        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        """ Handle the collision between two objects """
        #print('physicalObject.handle_collision_with (pre)')
        #print([self])
        #print([other_object])

        m1, m2 = self.radius**2, other_object.radius**2
        M = m1 + m2
        r1, r2 = self.r, other_object.r
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = self.v, other_object.v
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        self.v = u1
        other_object.v = u2
        self.vx = self.v[0]
        self.vy = self.v[1]
        other_object.vx = other_object.v[0]
        other_object.vy = other_object.v[1]
        #self.vx,self.vy = self.v[0], self.v[1]
        #other_object.vx, other_object.vy = other_object.v[0], other_object.v[1]
        #print('physicalObject.handle_collision_with (post)')
        #print([self])
        #print([other_object])
        #exit()

        # We're going to need a sequence of all of the pairs of particles when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.particles list of Particles on the fly.
        # pairs = combinations(range(self.n), 2)
        # for i,j in pairs:
            # obj_1 = game_objects[i]
            # obj_2 = game_objects[j]
            # if obj_1.collides_with(obj_2):
                # obj_1.handle_collision_with(obj_2, game_objects)
                # print('DLM: Obj1 collides with Obj2')
                # obj_2.handle_collision_with(obj_1, game_objects)
