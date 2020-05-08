from dataclasses import dataclass

import numpy as np
import pygame
from pygame.locals import QUIT

def crtify(rgbarray):
    # Pattern:
    # R G B
    # R G B
    # R G B

    original_size_x, original_size_y = rgbarray.shape[:2]
    new_rgbarray = np.zeros((original_size_x * 3, original_size_y * 3, 3))

    for original_x in range(0, original_size_x):
        for original_y in range(0, original_size_y):
            original_pixel = rgbarray[original_x, original_y,]
            for new_local_x in range(3):
                new_global_x = original_x * 3 + new_local_x
                for new_local_y in range(3):
                    new_global_y = original_y * 3 + new_local_y
                    new_rgbarray[new_global_x, new_global_y] = [0, 0, 0]
                    new_rgbarray[new_global_x, new_global_y, new_local_x] = original_pixel[new_local_x]

    return new_rgbarray

class Context():
    def __init__(self):
        self.frame_counter = 0
    
    def update(self):
        self.frame_counter += 1

CONTEXT = Context()
    
class Screen():
    def __init__(self):
        self._current_rgbarray = np.zeros((1,1))
    
    def get_current_array(self):
        return self._current_rgbarray

# def dim(rgbarray, amount):
#     rgbarray -= amount
#     rgbarray = rgbarray.clip(1, 40)

class ArraySubtractionTest(Screen):
    def __init__(self, rgbarray):
        self._current_rgbarray = np.copy(rgbarray)
        self.frames_before_dim = 10
    
    def update(self):
        if not CONTEXT.frame_counter % self.frames_before_dim:
            self._current_rgbarray -= 1
            self._current_rgbarray = self._current_rgbarray.clip(1, 255)

@dataclass
class CRTDrawerConfig():
    rgbarray: pygame.surfarray.array3d
    dim_delay: int = 2
    dim_amount: int = 3
    beam_sweep_amount: int = 80

class CRTDrawer(Screen):
    def __init__(self, config: CRTDrawerConfig):
        self._config = config
        self._ideal_rgbarray = crtify(self._config.rgbarray)
        self._size_x, self._size_y = self._ideal_rgbarray.shape[:2]
        self._current_rgbarray = np.zeros((self._size_x, self._size_y, 3))
        self._current_beam_position = [0, 0]

    def get_rgbarray_shape(self):
        return self._current_rgbarray.shape

    def update(self):
        # dim 
        if not CONTEXT.frame_counter % self._config.dim_delay:
            self._current_rgbarray -= self._config.dim_amount
            self._current_rgbarray = self._current_rgbarray.clip(1, 255)

        # redraw
        beam_positions = []
        new_beam_position = self._current_beam_position.copy()
        beam_pixels_to_draw = self._config.beam_sweep_amount
        while beam_pixels_to_draw > 0:
            pixels_left_on_current_row = self._size_x - new_beam_position[0]
            if beam_pixels_to_draw > pixels_left_on_current_row:
                beam_positions += [[x, new_beam_position[1]] for x in range(new_beam_position[0], new_beam_position[0] + pixels_left_on_current_row)]
                beam_pixels_to_draw -= pixels_left_on_current_row
                new_beam_position[1] = (new_beam_position[1] + 1) % self._size_y
                new_beam_position[0] = 0
            else:
                beam_positions += [[x, new_beam_position[1]] for x in range(new_beam_position[0], new_beam_position[0] + beam_pixels_to_draw)]
                beam_pixels_to_draw = 0

        for beam_position in beam_positions:
            self._current_rgbarray[beam_position[0], beam_position[1]] = self._ideal_rgbarray[beam_position[0], beam_position[1]]
        
        # update beam position
        self._current_beam_position = beam_positions[-1]

def main():
    imgsurface = pygame.image.load('sample_image.jpg')
    rgbarray = pygame.surfarray.array3d(imgsurface)

    crt_drawer_config = CRTDrawerConfig(
        rgbarray = rgbarray,
        dim_delay = 2,
        dim_amount = 3,
        beam_sweep_amount = 80000
    )

    crt_drawer = CRTDrawer(crt_drawer_config)
    screen = pygame.display.set_mode(crt_drawer.get_rgbarray_shape()[:2], 0, 32)
    
    pygame.display.set_caption("PyCRT")

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        crt_drawer.update()
        pygame.surfarray.blit_array(screen, crt_drawer.get_current_array())
        pygame.display.flip()

if __name__ == '__main__': 
    main()