import pygame

from engene import GameRenderLoop


class Checkbox:
    def __init__(self, render_loop, x, y, width, height, label):
        self.render_loop = render_loop
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.checked = False
        self.checkbox_square = render_loop.addImageFixedWidth("imgs/checkbox_square.png", x, y, width=width, height=height)
        self.checkbox_bg = render_loop.addImageFixedWidth("imgs/button_inactive.png", x + width + 10, y, width=200, height=height)
        self.checkbox_text = render_loop.addText(label, x + width + 30, y + height // 8, font_size=24, color=(255,255,255))
        self.checkbox_check = None
        self.render_loop.addClickListener(self.checkbox_square, self.handle_click)

    def is_checked(self):
        return self.checked

    def toggle(self):
        self.checked = not self.checked
        if self.checked:
            self.checkbox_check = self.render_loop.addImageFixedWidth("imgs/check_arrow.png", self.x, self.y, width=self.width, height=self.height)
        else:
            if self.checkbox_check:
                self.render_loop.removeElement(self.checkbox_check)
                self.checkbox_check = None

    def handle_click(self):
        self.toggle()

    def remove_from_renderloop(self):
        self.render_loop.removeElement(self.checkbox_square)
        self.render_loop.removeElement(self.checkbox_bg)
        self.render_loop.removeElement(self.checkbox_text)
        if self.checkbox_check:
            self.render_loop.removeElement(self.checkbox_check)

    def add_to_renderloop(self):
        self.checkbox_square = self.render_loop.addImageFixedWidth("imgs/checkbox_square.png", self.x, self.y, width=self.width, height=self.height)
        self.checkbox_bg = self.render_loop.addImageFixedWidth("imgs/checkbox_bg.png", self.x + self.width + 10, self.y, width=200, height=self.height)
        self.checkbox_text = self.render_loop.addText(self.label, self.x + self.width + 30, self.y + self.height // 2, font_size=24, color=(0, 0, 0))
        if self.checked:
            self.checkbox_check = self.render_loop.addImageFixedWidth("check.png", self.x, self.y, width=self.width, height=self.height)

class Button:
    def __init__(self, render_loop:GameRenderLoop, x, y, width, height, text, click_function,fg=(255, 255, 255),font_size=24,use_map_ofset=False):
        self.render_loop = render_loop
        self.x = x
        self.y = y
        self.keap_scedue=True
        self.width = width
        self.height = height
        self.text = text
        self.click_function = click_function
        self.is_hovered = False
        self.is_clicked = False

        self.button_inactive = render_loop.addImageFixedWidth("imgs/button_inactive.png", x, y, width=width, height=height,uses_map_offset=use_map_ofset)
        self.button_active = render_loop.addImageFixedWidth("imgs/button_active.png", x, y, width=width, height=height,uses_map_offset=use_map_ofset)
        self.button_clicked = render_loop.addImageFixedWidth("imgs/button_clicked.png", x, y, width=width, height=height,uses_map_offset=use_map_ofset)

        self.button_surface = render_loop.getSurface(self.button_inactive)
        self.button_surface_active = render_loop.getSurface(self.button_active)
        render_loop.hide(self.button_active)
        render_loop.hide(self.button_clicked)


        self.text_element = render_loop.addText(text, x + width // 2, y + height // 2, font_size=font_size, color=fg)


        self.render_loop.addSchadowIgnore(self.button_clicked)
        self.render_loop.addSchadowIgnore(self.button_inactive)
        self.render_loop.addSchadowIgnore(self.text_element)
        s=self.render_loop.getSurface(self.text_element)
        self.render_loop.moveto(self.text_element,(x + width // 2)-s.get_width()//2,( y + height // 2)-s.get_height()//2)

        self.cl_listener =self.render_loop.addClickListener(self.button_active, self.on_click)

        self.render_loop.set_scedue(self.hover_listen)
        #self.render_loop.addEventListener()
    def on_click(self):

        if self.is_hovered:
            #print("hover")
            #print(self.render_loop.elements)
            def hideClicked():
                self.render_loop.hide(self.button_clicked)
                self.render_loop.show(self.button_active)

                self.render_loop.lift(self.text_element)

            self.render_loop.after(100,hideClicked)
            self.render_loop.hide(self.button_active)
            self.render_loop.show(self.button_clicked)
            self.render_loop.lift(self.text_element)
        if self.click_function:
            self.click_function()



    def collides(self,surface, x, y):
        surface_rect = surface.get_rect()
        surface_rect.topleft = (x, y)

        mos_x, mos_y = pygame.mouse.get_pos()

        return surface_rect.collidepoint(mos_x, mos_y)

    def hover_listen(self):
        if not self.keap_scedue:
            return 3
        if self.is_hovered:
            #print("hover")
            #print(self.render_loop.elements)
            if not(self.collides(self.button_surface_active, self.x, self.y)):

                self.is_hovered=False


                self.render_loop.hide(self.button_active)
                self.render_loop.show(self.button_inactive)
                self.render_loop.lift(self.text_element)
                self.render_loop.hide(self.button_clicked)
        else:
            #print("nothovered")

            if (self.collides(self.button_surface, self.x, self.y)):
                self.is_hovered=True
                self.render_loop.show(self.button_active)
                self.render_loop.hide(self.button_inactive)
                self.render_loop.lift(self.text_element)

    def __hide__(self):
        self.keap_scedue=False
        def clear():
            for i in (self.button_clicked, self.button_active, self.button_inactive, self.text_element):
                self.render_loop.hide(i)

                self.render_loop.clearClickListener(self.cl_listener)
        self.render_loop.after(200,clear)

    def __remove__(self):
        self.render_loop.clearClickListener(self.cl_listener)
        return [self.button_active,self.button_inactive,self.button_clicked,self.text_element]







class ScheduleFunction():
    def __init__(self,function):
        self.function = function

    def __next__(self):
        print("test")
        while True:
            self.function()
            yield 0





class TextInput:
    def __init__(self, render_loop, x, y, width, height, placeholder):
        self.render_loop = render_loop
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.text = ""
        self.is_focused = False
        self.input_bg = render_loop.addImageFixedWidth("imgs/input_bg.png", x, y, width=width, height=height)
        self.text_element = None
        self.render_loop.addClickListener(self, self.handle_click)
        self.render_loop.addEventListener(pygame.KEYDOWN, self.handle_key)
        self.render_loop.addEventListener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_click)

    def handle_click(self):
        self.is_focused = True
        self.text_element = self.render_loop.addText("", self.x + 10, self.y + self.height // 2, font_size=24, color=(0, 0, 0))
        #self.render_loop.removeClickListener(self)
        self.render_loop.addEventListener(pygame.KEYDOWN, self.handle_key)
        self.render_loop.addEventListener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_click)

    def handle_key(self, event):
        if self.is_focused:
            if event.key == pygame.K_ESCAPE:
                self.finish_editing()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.finish_editing()
            else:
                self.text += event.unicode
            self.update_text_element()

    def handle_mouse_click(self, event):
        if not (self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height):
            self.finish_editing()

    def update_text_element(self):
        font = pygame.font.Font(None, 24)
        rendered_text = font.render(self.text, True, (0, 0, 0))
        text_width, _ = rendered_text.get_size()
        while text_width > self.width - 20:
            self.text = self.text[:-1]
            rendered_text = font.render(self.text, True, (0, 0, 0))
            text_width, _ = rendered_text.get_size()
        self.render_loop.removeElement(self.text_element)
        self.text_element = self.render_loop.addText(self.text, self.x + 10, self.y + self.height // 2, font_size=24, color=(0, 0, 0))

    def finish_editing(self):
        self.is_focused = False
        self.render_loop.removeElement(self.text_element)
        if not self.text:
            self.text_element = self.render_loop.addText(self.placeholder, self.x + 10, self.y + self.height // 2, font_size=24, color=(150, 150, 150))
        else:
            self.text_element = self.render_loop.addText(self.text, self.x + 10, self.y + self.height // 2, font_size=24, color=(0, 0, 0))
        self.render_loop.addClickListener(self, self.handle_click)
        self.render_loop.removeEventListeners(self)

    def get_text(self):
        return self.text

    def remove_from_renderloop(self):
        self.render_loop.removeElement(self.input_bg)
        if self.text_element:
            self.render_loop.removeElement(self.text_element)

    def add_to_renderloop(self):
        self.input_bg = self.render_loop.addImage("imgs/input_bg.png", self.x, self.y, width=self.width, height=self.height)
        if self.text:
            self.text_element = self.render_loop.addText(self.text, self.x + 10, self.y + self.height // 2, font_size=24, color=(0, 0, 0))
        else:
            self.text_element = self.render_loop.addText(self.placeholder, self.x + 10, self.y + self.height // 2, font_size=24, color=(150, 150, 150))
