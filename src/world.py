# -*- coding utf-8 -*-

from typing import Tuple, Optional, List

from struct import pack
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import moderngl as mgl
import pygame as pg

class World:

    def __init__(self, /, *, win_size: Optional[Tuple[int, int]]=(2560, 1440)) -> None:

        pg.display.set_mode(win_size, flags=pg.OPENGL | pg.DOUBLEBUF)

        self.ctx: mgl.Context = mgl.create_context()
        self.clock: pg.time.Clock = pg.time.Clock()

        try:

            with open('shaders/vertex.glsl', 'r') as vtx:
                vertex: str = vtx.read()
            with open('shaders/fragment.glsl', 'r') as frg:
                fragment: str = frg.read()

        except (OSError, FileNotFoundError, PermissionError) as _ :
            raise FileNotFoundError(f"Unable to read shaders.")

        self.program: mgl.Program = self.ctx.program(
            vertex_shader=vertex, fragment_shader=fragment)

        vertices: List[Tuple[int, int]] = [
            (-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1), (1, 1)
        ]

        vertex_data: bytes = pack(f'{len(vertices) * len(vertices[0])}f', *sum(vertices, ()))

        self.vbo: mgl.Buffer = self.ctx.buffer(vertex_data)
        self.vao: mgl.VertexArray = self.ctx.vertex_array(
            self.program, [(self.vbo, '2f', 'in_position')])

        self.set_uniform('u_resolution', win_size)

        self.alive = True

    def __repr__(self, /) -> str:
        return f'<object@{id(self)}:OpenGL_Program>'
    
    def __str__(self, /) -> str:
        return self.__repr__()
    
    def __del__(self, /) -> None:
        self.destroy()

    @property
    def alive(self, /) -> bool:
        return self.__alive
    
    @alive.setter
    def alive(self, value: bool, /) -> None:

        if isinstance(value, bool):
            self.__alive: bool = value

    def render(self, /) -> None:

        self.ctx.clear()
        self.vao.render()
        pg.display.flip()

    def update(self, /) -> None:
        self.set_uniform('u_time', pg.time.get_ticks() * 0.001)

    def run(self, /) -> None:

        while self.alive:

            self.check_events()
            self.update()
            self.render()
            self.clock.tick(0)

            fps: float = self.clock.get_fps()
            pg.display.set_caption(f'{fps :.1f}')

    def set_uniform(self, u_name: str, u_value: float, /) -> None:

        try: self.program[u_name] = u_value
        except KeyError as _ : ...

    def destroy(self, /) -> None:
        
        try:

            self.vbo.release()
            self.program.release()
            self.vao.release()

        except Exception as _ : ...

    def check_events(self, /) -> None:

        for event in pg.event.get():

            if event.type == pg.QUIT or (
               event.type == pg.KEYDOWN
               and event.key == pg.K_ESCAPE):

                self.destroy()
                pg.quit()

                raise SystemExit(0)
