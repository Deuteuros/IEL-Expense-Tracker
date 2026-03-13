import flet as ft
import database
import pandas as pd
from datetime import datetime
import locale

# Fallback for month names if locale is not set to FR/MG
MONTHS_MG = {
    1: "Janoary", 2: "Febroary", 3: "Martsa", 4: "Aprily",
    5: "Mey", 6: "Jona", 7: "Jolay", 8: "Aogositra",
    9: "Septambra", 10: "Oktobra", 11: "Novambra", 12: "Desambra"
}

DAYS_MG = {
    "Monday": "Alatsinainy", "Tuesday": "Talata", "Wednesday": "Alarobia",
    "Thursday": "Kamisary", "Friday": "Zoma", "Saturday": "Sabotsy", "Sunday": "Alahady"
}

class HistoryView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=0)
        self.main_page = page
        self.selection_mode = False
        self._selected_indices = []
        
        # Initial State: Selected Month/Year
        df = database.get_df()
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            latest = df['date'].max()
            self.selected_month = latest.month
            self.selected_year = latest.year
        else:
            now = datetime.now()
            self.selected_month = now.month
            self.selected_year = now.year

        self.refresh(update=False)

    def refresh(self, update=True):
        self.controls.clear()
        df = database.get_df()
        
        # Header
        header_content = []
        if self.selection_mode:
            header_content = [
                ft.IconButton(ft.Icons.CLOSE, on_click=self.exit_selection_mode),
                ft.Text(f"{len(self._selected_indices)} voafidy", size=18, weight="bold"),
                ft.Row([
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=self.confirm_delete),
                ])
            ]
        else:
            header_content = [
                ft.Text("Transactions", size=28, weight="bold"),
                ft.Row([
                    ft.IconButton(ft.Icons.FILTER_LIST),
                    ft.IconButton(ft.Icons.SEARCH),
                ])
            ]

        self.controls.append(
            ft.Container(
                content=ft.Row(header_content, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=20, right=10, top=10, bottom=10)
            )
        )

        if df.empty:
            self.controls.append(ft.Container(content=ft.Text("Tsy mbola misy angona.", size=16), padding=20))
            if update: self.update()
            return

        df['date'] = pd.to_datetime(df['date'])
        
        # --- 1. Horizontal Month Selector ---
        # Get unique months/years present in data
        df['year_month'] = df['date'].dt.to_period('M')
        available_periods = pd.PeriodIndex(df['year_month'].unique()).sort_values()
        
        month_items = []
        for period in available_periods:
            is_selected = (period.month == self.selected_month and period.year == self.selected_year)
            
            # Label
            month_name = MONTHS_MG.get(period.month, period.strftime('%b'))
            month_label = month_name.lower() if month_name else "---"
            year_label = str(period.year) if period.year != datetime.now().year else ""
            
            month_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(month_label, 
                                color=ft.Colors.BLACK if is_selected else ft.Colors.GREY_500,
                                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                                size=16),
                        ft.Container(
                            height=3, width=40,
                            bgcolor=ft.Colors.BLACK if is_selected else ft.Colors.TRANSPARENT,
                            border_radius=2
                        ) if is_selected else ft.Container(height=3)
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(horizontal=15),
                    on_click=lambda e, m=period.month, y=period.year: self.change_period(m, y)
                )
            )

        self.controls.append(
            ft.Container(
                content=ft.Row(month_items, scroll=ft.ScrollMode.HIDDEN),
                padding=ft.padding.only(bottom=10)
            )
        )

        # Filter Data for Selected Period
        mask = (df['date'].dt.month == self.selected_month) & (df['date'].dt.year == self.selected_year)
        month_df = df[mask].copy()

        # --- 2. Summary Bar ---
        total_income = month_df[month_df['categorie_flux'].isin(['Income', 'Miditra'])]['montant_total_mga'].sum()
        total_expense = month_df[month_df['categorie_flux'].isin(['Expense', 'Fandaniana'])]['montant_total_mga'].sum()
        total_net = total_income - total_expense

        summary_bar = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.RED_400, size=20),
                    ft.Text(f"{total_expense:,.0f} MGA", color=ft.Colors.RED_700, size=13, weight="bold"),
                ], spacing=2),
                ft.Row([
                    ft.Icon(ft.Icons.ARROW_DROP_UP, color=ft.Colors.GREEN_400, size=20),
                    ft.Text(f"{total_income:,.0f} MGA", color=ft.Colors.GREEN_700, size=13, weight="bold"),
                ], spacing=2),
                ft.Text(f"= {total_net:,.0f} MGA", color=ft.Colors.BLACK, size=13, weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            bgcolor="#E1F0F7",
            padding=8,
            border_radius=10,
            margin=ft.margin.symmetric(horizontal=20, vertical=5)
        )
        self.controls.append(summary_bar)

        # --- 3. Daily Grouped List ---
        list_items = []
        if month_df.empty:
            list_items.append(ft.Container(content=ft.Text("Tsy misy hetsika tamin'ity volana ity.", size=14, color=ft.Colors.GREY_400), alignment=ft.alignment.center, padding=40))
        else:
            month_df = month_df.sort_values(by='date', ascending=False)
            for day, day_df in month_df.groupby(month_df['date'].dt.date, sort=False):
                # Day Total logic
                day_income = day_df[day_df['categorie_flux'].isin(['Income', 'Miditra'])]['montant_total_mga'].sum()
                day_expense = day_df[day_df['categorie_flux'].isin(['Expense', 'Fandaniana'])]['montant_total_mga'].sum()
                day_net = day_income - day_expense
                
                # Day Header
                eng_day = day.strftime('%A')
                mg_day = DAYS_MG.get(eng_day, eng_day)
                day_label = f"{mg_day} {day.day} {month_label}"
                list_items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{day_label}", color=ft.Colors.GREY_500, size=14),
                            ft.Text(f"{day_net:,.0f} MGA", color=ft.Colors.GREY_600, size=14),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.only(left=20, right=20, top=15, bottom=5)
                    )
                )
                
                # Transactions
                for idx, row in day_df.iterrows():
                    list_items.append(self.create_transaction_card(idx, row))
        
        self.controls.append(
            ft.Column(list_items, scroll=ft.ScrollMode.AUTO, expand=True, spacing=0)
        )
        
        if update:
            self.update()

    def create_transaction_card(self, idx, row):
        is_income = row['categorie_flux'] in ["Income", "Miditra"]
        
        # Color & Icon based on Category (Basic mapping)
        icon = ft.Icons.SHOPPING_BAG
        bg_color = ft.Colors.ORANGE_100
        icon_color = ft.Colors.ORANGE_700
        
        if is_income:
            icon = ft.Icons.ATTACH_MONEY
            bg_color = ft.Colors.PURPLE_100
            icon_color = ft.Colors.PURPLE_700
        elif "riz" in row['item'].lower() or "beignet" in row['item'].lower():
            icon = ft.Icons.FASTFOOD
            bg_color = ft.Colors.GREEN_100
            icon_color = ft.Colors.GREEN_700
        elif row['item'].isdigit(): # Like "194", "166" in some logs
            icon = ft.Icons.DIRECTIONS_BUS
            bg_color = ft.Colors.ORANGE_200
            icon_color = ft.Colors.ORANGE_800

        leading = None
        if self.selection_mode:
            leading = ft.Checkbox(
                value=idx in self._selected_indices,
                on_change=lambda e, i=idx: self.toggle_selection(i)
            )
        else:
            leading = ft.Container(
                content=ft.Icon(icon, color=icon_color, size=24),
                width=48, height=48,
                bgcolor=bg_color,
                border_radius=24,
            )

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    leading,
                    ft.Column([
                        ft.Text(row['item'], weight="bold", size=16),
                        ft.Text(f"{row['quantite']} {row['unite']}" if row['unite'] else f"{row['quantite']}", size=13, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], spacing=15),
                ft.Text(
                    f"{'- ' if not is_income else '+ '}{row['montant_total_mga']:,.0f} MGA",
                    color=ft.Colors.RED_500 if not is_income else ft.Colors.GREEN_600,
                    weight="bold",
                    size=16
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            on_long_press=lambda e, i=idx: self.enter_selection_mode(i),
            on_click=lambda e, i=idx: self.handle_click(i)
        )

    def change_period(self, month, year):
        self.selected_month = month
        self.selected_year = year
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
