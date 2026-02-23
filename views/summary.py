import flet as ft
import database

def get_summary_view():
    income, expense, balance = database.get_summary_data()
    
    def create_card(title, value, color, icon):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=30),
                ft.Text(title, size=14, color=ft.Colors.GREY_700),
                ft.Text(f"Ar {value:,.0f}", size=22, weight="bold"),
            ], spacing=5),
            padding=20,
            border_radius=15,
            bgcolor="surfacevariant",
            expand=True,
        )

    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Manao ahoana!", size=28, weight="bold"),
                padding=ft.Padding.only(left=20, top=40, bottom=10)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Caisse", size=16, color=ft.Colors.GREY_700),
                    ft.Text(f"Ar {balance:,.0f}", size=36, weight="bold", color=ft.Colors.GREEN_700 if balance >= 0 else ft.Colors.RED_700),
                ]),
                padding=20,
                alignment=ft.Alignment(0,0),
            ),
            ft.Row([
                create_card("Miditra", income, ft.Colors.GREEN, ft.Icons.ARROW_DOWNWARD),
                create_card("Fandaniana", expense, ft.Colors.RED, ft.Icons.ARROW_UPWARD),
            ], spacing=10),
        ], scroll=ft.ScrollMode.AUTO, expand=True),
        padding=10,
        expand=True
    )
