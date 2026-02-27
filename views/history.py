import flet as ft
import database
import pandas as pd
from datetime import datetime

class HistoryView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.main_page = page
        self.selection_mode = False
        self._selected_indices = [] # Use list instead of set for Flet Web serialization
        self.filter_type = "Hafakely"
        self.refresh(update=False)

    def refresh(self, update=True):
        self.controls.clear()
        df = database.get_df()
        
        # Header
        header_content = []
        if self.selection_mode:
            header_content = [
                ft.IconButton(ft.Icons.CLOSE, on_click=self.exit_selection_mode),
                ft.Text(f"{len(self._selected_indices)} voafidy", size=20, weight="bold"),
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

        if not self.selection_mode:
            # Re-mapping filter type to tab index
            filter_map = {"Hafakely": 0, "Herinandro": 1, "Volana": 2, "Taona": 3}
            tab_index = filter_map.get(self.filter_type, 0)
            
            self.controls.append(
                ft.Container(
                    content=ft.Tabs(
                        selected_index=tab_index,
                        on_change=self.on_filter_change,
                        tabs=[
                            ft.Tab(text="Rehetra"),
                            ft.Tab(text="Herinandro"),
                            ft.Tab(text="Volana"),
                            ft.Tab(text="Taona"),
                        ],
                    ),
                    padding=ft.Padding(10, 0, 10, 10)
                )
            )

        # List Container
        list_items = []
        if df.empty:
            list_items.append(ft.Text("Tsy mbola misy angona.", size=16))
        else:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False)
            
            if self.filter_type == "Herinandro":
                df['group'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time.strftime('%Y-W%W'))
            elif self.filter_type == "Volana":
                df['group'] = df['date'].dt.strftime('%B %Y')
            elif self.filter_type == "Taona":
                df['group'] = df['date'].dt.strftime('%Y')
            else:
                df['group'] = None

            if df['group'].notnull().any() and not self.selection_mode:
                for group_name, group_df in df.groupby('group', sort=False):
                    list_items.append(
                        ft.Container(
                            content=ft.Text(group_name, weight="bold", size=18, color=ft.Colors.GREEN_700),
                            padding=ft.Padding(10, 20, 10, 5)
                        )
                    )
                    for idx, row in group_df.iterrows():
                        list_items.append(self.create_tile(idx, row))
            else:
                for idx, row in df.iterrows():
                    list_items.append(self.create_tile(idx, row))
        
        self.controls.append(
            ft.Column(list_items, scroll=ft.ScrollMode.AUTO, expand=True)
        )
        
        if update:
            self.update()

    def create_tile(self, idx, row):
        is_income = row['categorie_flux'] in ["Income", "Miditra"]
        display_name = f"{row['item']} - {row['quantite']}{row['unite']}" if row['unite'] else f"{row['item']} - {row['quantite']}"
        
        leading = None
        if self.selection_mode:
            leading = ft.Checkbox(
                value=idx in self._selected_indices,
                on_change=lambda e, i=idx: self.toggle_selection(i)
            )
        else:
            leading = ft.CircleAvatar(
                content=ft.Icon(ft.Icons.SHOPPING_BASKET if not is_income else ft.Icons.ATTACH_MONEY, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN if is_income else ft.Colors.RED_400,
            )

        return ft.ListTile(
            leading=leading,
            title=ft.Text(display_name, weight="bold"),
            subtitle=ft.Text(f"{row['date'].strftime('%Y-%m-%d')} | {row['fournisseur_client'] or '---'}"),
            trailing=ft.Text(
                f"{' + ' if is_income else ' - '} Ar {row['montant_total_mga']:,.0f}",
                color=ft.Colors.GREEN if is_income else ft.Colors.RED,
                weight="bold"
            ),
            on_long_press=lambda e, i=idx: self.enter_selection_mode(i),
            on_click=lambda e, i=idx: self.handle_click(i)
        )

    def on_filter_change(self, e):
        idx = e.control.selected_index
        filter_reverse_map = {0: "Hafakely", 1: "Herinandro", 2: "Volana", 3: "Taona"}
        self.filter_type = filter_reverse_map.get(idx, "Hafakely")
        self.refresh()

    def enter_selection_mode(self, index):
        if not self.selection_mode:
            self.selection_mode = True
            if index not in self._selected_indices:
                self._selected_indices.append(index)
            self.refresh()

    def exit_selection_mode(self, e=None):
        self.selection_mode = False
        self._selected_indices = []
        self.refresh()

    def toggle_selection(self, index):
        if index in self._selected_indices:
            self._selected_indices.remove(index)
        else:
            self._selected_indices.append(index)
        
        if not self._selected_indices:
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
            database.delete_entries_by_index(self._selected_indices)
            dlg.open = False
            self.exit_selection_mode()
            if hasattr(self.main_page, "refresh_view"):
                self.main_page.refresh_view()
            self.main_page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Famafana"),
            content=ft.Text(f"Tena hofafanao ve ireto {len(self._selected_indices)} voafidy ireto?"),
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
