# Simple drag from a boxlayout onto a drop zone, animate the return if the drop zone is missed.
#reorganize.....


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation



kv = """
<DragButton>:
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 10
    on_release: print(f'Drag Button {self.text} pressed')

BoxLayout:
    BoxLayout:
        orientation: 'vertical'
        dragging: False
        DragButton:
            text: '0'
        DragButton:
            text: '1'
        DragButton:
            text: '2'
        DragButton:
            text: '3'
        DragButton:
            text: '4'
        DragButton:
            text: '5'
        DragButton:
            text: '6'
        DragButton:
            text: '7'
        DragButton:
            text: '8'
    BoxLayout:
        id: middle
    BoxLayout:
        id:right
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Do Nothing'
            Label:
                id: remove_zone
                text: 'Remove Widget'
"""
# comment from Tshirtman on using the touch.ud[]
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
            self.parent.dragging = True   # global drag indicator
            self.parent.dragwig  = self

        if (      self.parent.dragging
          and not self.dragging
          and     self.collide_point(*touch.pos) 
           ):
            idx = self.parent.children.index(self)
            #below = touch.y < self.center_y
            #print('i am in child', idx, 'below?', below)
            self.parent.remove_widget(self.parent.dragwig)
            self.parent.add_widget(self.parent.dragwig, index=idx)
        super().on_touch_move(touch)
        return False

    def on_touch_up(self, touch):
        app = App.get_running_app()
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            self.parent.dragging = False
            if self.collide_widget(app.root.ids.remove_zone):
                self.parent.remove_widget(self)
            else:
                #anim = Animation(pos=self.original_pos, duration=1)
                #anim.start(self)
                self.parent.do_layout()
        return super().on_touch_up(touch)


class DragTestApp(App):
    def build(self):
        return Builder.load_string(kv)


DragTestApp().run()
