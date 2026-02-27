import flet as ft
import database
import pandas as pd
from datetime import datetime

def get_history_view():
    df = database.get_df()
    
    # State for filtering
    filter_state = ft.Ref[ft.SegmentedButton]()
    list_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def build_list(filter_type="Hafakely"): # Default to All/Recent if not grouped
        df = database.get_df()
        if df.empty:
            return [ft.Text("Tsy mbola misy angona.", size=16)]
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)
        
        items = []
        
        if filter_type == "Herinandro":
            # Group by week
            df['group'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time.strftime('%Y-W%W'))
        elif filter_type == "Volana":
            # Group by month
            df['group'] = df['date'].dt.strftime('%B %Y')
        elif filter_type == "Taona":
            # Group by year
            df['group'] = df['date'].dt.strftime('%Y')
        else:
            df['group'] = None

        if df['group'].notnull().any():
            for group_name, group_df in df.groupby('group', sort=False):
                items.append(
                    ft.Container(
                        content=ft.Text(group_name, weight="bold", size=18, color=ft.Colors.GREEN_700),
                        padding=ft.Padding(10, 20, 10, 5)
                    )
                )
                for _, row in group_df.iterrows():
                    items.append(create_tile(row))
        else:
            for _, row in df.iterrows():
                items.append(create_tile(row))
        
        return items

    def create_tile(row):
        is_income = row['categorie_flux'] in ["Income", "Miditra"]
        # Format: "Item - QtyUnit"
        display_name = f"{row['item']} - {row['quantite']}{row['unite']}" if row['unite'] else f"{row['item']} - {row['quantite']}"
        
        return ft.ListTile(
            leading=ft.CircleAvatar(
                content=ft.Icon(ft.Icons.SHOPPING_BASKET if not is_income else ft.Icons.ATTACH_MONEY, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN if is_income else ft.Colors.RED_400,
            ),
            title=ft.Text(display_name, weight="bold"),
            subtitle=ft.Text(f"{row['date'].strftime('%Y-%m-%d')} | {row['fournisseur_client'] or '---'}"),
            trailing=ft.Text(
                f"{' + ' if is_income else ' - '} Ar {row['montant_total_mga']:,.0f}",
                color=ft.Colors.GREEN if is_income else ft.Colors.RED,
                weight="bold"
            ),
        )

    def on_filter_change(e):
        selected = list(e.control.selected)[0]
        list_container.controls = build_list(selected)
        list_container.update()

    filter_menu = ft.SegmentedButton(
        ref=filter_state,
        segments=[
            ft.Segment(value="Hafakely", label=ft.Text("Rehetra")),
            ft.Segment(value="Herinandro", label=ft.Text("Herinandro")),
            ft.Segment(value="Volana", label=ft.Text("Volana")),
            ft.Segment(value="Taona", label=ft.Text("Taona")),
        ],
        selected=["Hafakely"],
        on_change=on_filter_change,
    )

    list_container.controls = build_list("Hafakely")

    return ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("Tantara", size=24, weight="bold"),
                filter_menu,
            ]),
            padding=20
        ),
        list_container
    ], expand=True)
