import os
import pygame
import gcore.globalvars as g


class LTexture:
    def __init__(self, texture_name: str = None, texture_text: str = None, color: tuple = None, is_small_font = False):
        self._surface = None # protected instance member

        if texture_text and color:
            if is_small_font:
                self._surface = g.font_small.render(texture_text, 1, color).convert_alpha()
            else:
                self._surface = g.font.render(texture_text, 1, color).convert_alpha()
        elif texture_name:
            # convert() or convert_alpha() help a bit to make pixel_format more efficient for rendering
            self._surface = pygame.image.load(os.path.join('textures', texture_name)).convert_alpha()
            if color:
                self.SetColor(*color)


    # very slow func
    def SetColor(self, r, g, b):
        w, h = self._surface.get_size()
        for x in range(w):
            for y in range(h):
                a = self._surface.get_at((x, y))[3]
                self._surface.set_at((x, y), pygame.Color(r, g, b, a))


    def ReplaceColor(self, src_color, dst_color):
        sr, sg, sb = src_color
        dr, dg, db = dst_color
        w, h = self._surface.get_size()
        for x in range(w):
            for y in range(h):
                a = self._surface.get_at((x, y))[3]
                if self._surface.get_at((x, y))[0] == sr and self._surface.get_at((x, y))[1] == sg and self._surface.get_at((x, y))[2] == sb:
                    self._surface.set_at((x, y), pygame.Color(dr, dg, db, a))


    def Render(self, x = 0, y = 0, facing: float = 0.0):
        if facing != 0.0:
            rotated_surface = pygame.transform.rotate(self._surface, facing * 90.0)
            g.window.blit(rotated_surface, (x, y))
        else:
            g.window.blit(self._surface, (x, y))


class LTextureFrames(LTexture):
    def __init__(self, w, h, horizontal = True, texture_name: str = None, texture_text: str = None, color: tuple = None, is_small_font = False):
        super(LTextureFrames, self).__init__(texture_name, texture_text, color, is_small_font)
            
        self.__frames = []
        x = 0
        y = 0
        if horizontal:
            while x < self._surface.get_width():
                self.__frames.append(self._surface.subsurface(pygame.Rect(x, y, w, h)))
                x += w
        else:
            while y < self._surface.get_height():
                self.__frames.append(self._surface.subsurface(pygame.Rect(x, y, w, h)))
                y += h


    def GetSize(self):
        return len(self.__frames)


    def RenderFrame(self, index, x = 0, y = 0, facing: float = 0.0):
        if index < len(self.__frames):
            if facing != 0.0:
                rotated_surface = pygame.transform.rotate(self.__frames[index], facing * 90.0)
                g.window.blit(rotated_surface, (x, y))
            else:
                g.window.blit(self.__frames[index], (x, y))
        