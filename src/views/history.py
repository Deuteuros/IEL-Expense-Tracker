import flet as ft
import database
from datetime import datetime

# Fallback for month names
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
        
        # Initial State: Selected Month/Year from the newest data
        available_months = database.get_months_with_data()
        if available_months:
            self.selected_month_str = available_months[0] # e.g., '2026-04'
        else:
            self.selected_month_str = datetime.now().strftime("%Y-%m")

        self.refresh(update=False)

    def refresh(self, update=True):
        self.controls.clear()
        
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
                ft.Text("Tantara", size=28, weight="bold"),
                ft.Row([
                    ft.IconButton(ft.Icons.SEARCH),
                ])
            ]

        self.controls.append(
            ft.Container(
                content=ft.Row(header_content, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=20, right=10, top=10, bottom=10)
            )
        )

        available_months = database.get_months_with_data()
        
        if not available_months:
            self.controls.append(ft.Container(content=ft.Text("Tsy mbola misy hetsika voasoratra.", size=16), padding=40))
            if update: self.update()
            return

        # --- 1. Horizontal Month Selector (Dynamic) ---
        month_items = []
        for month_s in reversed(available_months): # Past to Present
            is_selected = (month_s == self.selected_month_str)
            
            y, m = map(int, month_s.split('-'))
            month_name = MONTHS_MG.get(m, str(m))
            month_label = month_name.lower()
            year_label = str(y) if y != datetime.now().year else ""
            
            month_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(month_label, 
                                color=ft.Colors.BLACK if is_selected else ft.Colors.GREY_500,
                                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                                size=16),
                        ft.Container(
                            height=3, width=40,
                            bgcolor=ft.Colors.GREEN_700 if is_selected else ft.Colors.TRANSPARENT,
                            border_radius=2
                        )
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(horizontal=15),
                    on_click=lambda e, s=month_s: self.change_period(s)
                )
            )

        self.controls.append(
            ft.Container(
                content=ft.Row(list(reversed(month_items)), scroll=ft.ScrollMode.HIDDEN), # Present first
                padding=ft.padding.only(bottom=10)
            )
        )

        # Fetch Data for Selected Period
        month_df = database.get_transactions_by_month(self.selected_month_str)

        # --- 2. Summary Bar ---
        total_income = month_df[month_df['categorie_flux'].isin(['Miditra', 'Vente'])]['montant_total_mga'].sum()
        total_expense = month_df[month_df['categorie_flux'].isin(['Fandaniana', 'Achat'])]['montant_total_mga'].sum()
        total_net = total_income - total_expense

        summary_bar = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.RED_400, size=20),
                    ft.Text(f"{total_expense:,.0f} Ar", color=ft.Colors.RED_700, size=13, weight="bold"),
                ], spacing=2),
                ft.Row([
                    ft.Icon(ft.Icons.ARROW_DROP_UP, color=ft.Colors.GREEN_400, size=20),
                    ft.Text(f"{total_income:,.0f} Ar", color=ft.Colors.GREEN_700, size=13, weight="bold"),
                ], spacing=2),
                ft.Text(f"= {total_net:,.0f} Ar", color=ft.Colors.BLACK, size=13, weight="bold"),
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
            list_items.append(ft.Container(content=ft.Text("Tsy misy hetsika.", size=14), padding=40))
        else:
            # Group by formatted date
            for day_str, day_df in month_df.groupby('date', sort=False):
                # Day Total
                day_income = day_df[day_df['categorie_flux'].isin(['Miditra', 'Vente'])]['montant_total_mga'].sum()
                day_expense = day_df[day_df['categorie_flux'].isin(['Fandaniana', 'Achat'])]['montant_total_mga'].sum()
                day_net = day_income - day_expense
                
                # Day Header
                dt = datetime.strptime(day_str, "%Y-%m-%d")
                eng_day = dt.strftime('%A')
                mg_day = DAYS_MG.get(eng_day, eng_day)
                month_name_mg = MONTHS_MG.get(dt.month, "").lower()
                day_label = f"{mg_day} {dt.day} {month_name_mg}"
                
                list_items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(day_label, color=ft.Colors.GREY_500, size=14),
                            ft.Text(f"{day_net:,.0f} Ar", color=ft.Colors.GREY_600, size=14),
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
        is_income = row['categorie_flux'] in ["Income", "Miditra", "Vente"]
        
        # UI logic: Icon selection
        icon = ft.Icons.SHOPPING_BAG
        bg_color = ft.Colors.ORANGE_100
        icon_color = ft.Colors.ORANGE_700
        
        if is_income:
            icon = ft.Icons.ATTACH_MONEY
            bg_color = ft.Colors.GREEN_100
            icon_color = ft.Colors.GREEN_700
        
        # Simple specific item styling
        item_lower = str(row['item']).lower()
        if any(x in item_lower for x in ["bus", "taxi", "transport"]):
            icon = ft.Icons.DIRECTIONS_BUS
            bg_color = ft.Colors.BLUE_100
            icon_color = ft.Colors.BLUE_700

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=icon_color, size=24),
                        width=48, height=48,
                        bgcolor=bg_color,
                        border_radius=24,
                    ),
                    ft.Column([
                        ft.Text(row['item'], weight="bold", size=16),
                        ft.Text(f"{row['quantite']} {row['unite']}" if row['unite'] else f"{row['quantite']}", size=13, color=ft.Colors.GREY_600),
                    ], spacing=2)
                ], spacing=15),
                ft.Text(
                    f"{'- ' if not is_income else '+ '}{row['montant_total_mga']:,.0f} Ar",
                    color=ft.Colors.RED_500 if not is_income else ft.Colors.GREEN_600,
                    weight="bold",
                    size=16
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            on_click=lambda e: print(f"Clicked {row['item']}")
        )

    def change_period(self, month_str):
        self.selected_month_str = month_str
        self.refresh()

    def exit_selection_mode(self, e=None):
        self.selection_mode = False
        self._selected_indices = []
        self.refresh()

    def confirm_delete(self, e):
        # Basic placeholder for refactored delete logic
        pass

def get_history_view(page: ft.Page):
    return HistoryView(page)
