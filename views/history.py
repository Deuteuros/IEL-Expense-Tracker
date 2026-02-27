import flet as ft
import database

class HistoryView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.main_page = page
        self.selection_mode = False
        self.selected_indices = set()
        self.refresh(update=False)

    def refresh(self, update=True):
        self.controls.clear()
        df = database.get_df()
        
        # Header
        header_content = []
        if self.selection_mode:
            header_content = [
                ft.IconButton(ft.Icons.CLOSE, on_click=self.exit_selection_mode),
                ft.Text(f"{len(self.selected_indices)} voafidy", size=20, weight="bold"),
                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=self.confirm_delete),
            ]
        else:
            header_content = [
                ft.Text("Tantara", size=24, weight="bold"),
            ]

        self.controls.append(
            ft.Container(
                content=ft.Row(header_content, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=20
            )
        )

        # List Items
        items = []
        # Reverse data to see latest first, but keep track of original index
        for idx, row in df.iloc[::-1].iterrows():
            is_income = row['Type'] in ["Income", "Miditra"]
            
            leading = None
            if self.selection_mode:
                leading = ft.Checkbox(
                    value=idx in self.selected_indices,
                    on_change=lambda e, i=idx: self.toggle_selection(i)
                )
            else:
                leading = ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.MONEY, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN if is_income else ft.Colors.RED,
                )

            items.append(
                ft.ListTile(
                    leading=leading,
                    title=ft.Text(row['Category'], weight="bold"),
                    subtitle=ft.Text(row['Date']),
                    trailing=ft.Text(
                        f"{' + ' if is_income else ' - '} Ar {row['Amount']:,.0f}",
                        color=ft.Colors.GREEN if is_income else ft.Colors.RED,
                        weight="bold"
                    ),
                    on_long_press=lambda e, i=idx: self.enter_selection_mode(i),
                    on_click=lambda e, i=idx: self.handle_click(i)
                )
            )
        
        self.controls.append(
            ft.Column(items, scroll=ft.ScrollMode.AUTO, expand=True)
        )
        if update:
            self.update()

    def enter_selection_mode(self, index):
        if not self.selection_mode:
            self.selection_mode = True
            self.selected_indices.add(index)
            self.refresh()

    def exit_selection_mode(self, e=None):
        self.selection_mode = False
        self.selected_indices.clear()
        self.refresh()

    def toggle_selection(self, index):
        if index in self.selected_indices:
            self.selected_indices.remove(index)
        else:
            self.selected_indices.add(index)
        
        if not self.selected_indices:
            self.selection_mode = False
        self.refresh()

    def handle_click(self, index):
        if self.selection_mode:
            self.toggle_selection(index)

    def confirm_delete(self, e):
        def close_dlg(e):
            dlg.open = False
            self.main_page.update()

        def delete_confirmed(e):
            database.delete_entries_by_index(list(self.selected_indices))
            dlg.open = False
            self.exit_selection_mode()
            # Try to refresh the global view if possible
            if hasattr(self.main_page, "refresh_view"):
                self.main_page.refresh_view()
            self.main_page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Famafana"),
            content=ft.Text(f"Tena hofafanao ve ireto {len(self.selected_indices)} ireto?"),
            actions=[
                ft.TextButton("Tsia", on_click=close_dlg),
                ft.TextButton("Eny", on_click=delete_confirmed),
            ]
        )
        self.main_page.overlay.append(dlg)
        dlg.open = True
        self.main_page.update()

def get_history_view(page: ft.Page):
    return HistoryView(page)
