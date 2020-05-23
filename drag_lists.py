from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation


kv = """
<DragButton>:
    size_hint_y: None
    height: 48
    font_size: 20
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 10
    on_press: print(f'Drag Button {self.text} pressed, wid: {self}')

BoxLayout:
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            drag_type: ['content']
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                id: sv_left
    Label:
        text: 'Drag to reorder a ScrollView'
        # size_hint_x: .25
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            drag_type: ['content']
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                id: sv_right
            
"""
# it's always a good idea to create your unique key in the ud, as other widgets can also read and write to it
# i've always used some scheme like '{prefix}-{widget_id}-{qualifier}' as keys for that in my apps


class DragButton(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('on touch down')
            self.original_pos = self.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.opacity = 0.4
            self.dragging = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        app = App.get_running_app()
        if self.dragging:
            self.opacity = 1
            self.dragging = False

            # if self.collide_widget(app.root.ids.remove_zone):
            #     self.parent.remove_widget(self)
            # else:
            #     anim = Animation(pos=self.original_pos, duration=1)
            #     anim.start(self)
        return super().on_touch_up(touch)


class DragTest2App(App):
    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        for i in range(100):
            w = DragButton(text='L'+str(i))
            self.root.ids.sv_left.add_widget(w)
            w = DragButton(text='R' + str(i))
            self.root.ids.sv_right.add_widget(w)




DragTest2App().run()