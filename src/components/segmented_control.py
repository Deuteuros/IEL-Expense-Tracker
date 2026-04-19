import flet as ft

class CustomSegmentedControl(ft.Container):
    def __init__(self, segments, selected_index=0, on_change=None):
        super().__init__()
        self.segments = segments
        self.selected_index = selected_index
        self.on_change = on_change
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)
        self.border_radius = 25
        self.padding = 4
        self.content = ft.Row(spacing=0, tight=True)
        self.build_segments()

    def build_segments(self):
        self.content.controls = []
        for i, seg in enumerate(self.segments):
            is_selected = i == self.selected_index
            self.content.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(seg.icon, size=18) if hasattr(seg, "icon") and seg.icon else ft.Container(),
                        ft.Text(seg.label, weight="bold" if is_selected else None),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.Colors.WHITE if is_selected else ft.Colors.TRANSPARENT,
                    border_radius=20,
                    padding=ft.padding.symmetric(15, 10),
                    on_click=lambda e, idx=i: self.select(idx),
                    animate=ft.Animation(300, "decelerate"),
                    expand=True,
                )
            )

    def select(self, index):
        self.selected_index = index
        self.build_segments()
        self.update()
        if self.on_change:
            # Simulate an event object with a value property
            class Event:
                def __init__(self, val, ctrl):
                    self.value = val
                    self.control = ctrl
            self.on_change(Event(self.segments[index].value, self))

class Segment:
    def __init__(self, value, label, icon=None):
        self.value = value
        self.label = label
        self.icon = icon
