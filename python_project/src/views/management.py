import flet as ft
import database

def get_management_view(page: ft.Page):
    return ft.Container(
        content=ft.Column([
            # Header
            ft.Container(
                content=ft.Text("Fikirakirana (Gestion)", size=24, weight="bold"),
                padding=ft.Padding.only(left=10, top=10, bottom=10)
            ),

            # CSV Data Management
            ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.STORAGE),
                        title=ft.Text("Dataly CSV", weight="bold"),
                        subtitle=ft.Text("Hanafatra na handefa ny angona rehetra"),
                    ),
                    ft.Divider(),
                    ft.Row([
                        ft.FilledButton(
                            "Hanafatra (Import)", 
                            icon=ft.Icons.UPLOAD_FILE, 
                            on_click=page.trigger_import,
                            expand=True
                        ),
                        ft.FilledButton(
                            "Handefa (Export)", 
                            icon=ft.Icons.DOWNLOAD, 
                            on_click=page.trigger_export,
                            expand=True
                        ),
                    ], spacing=10),
                ]),
                padding=15,
                bgcolor="surfacevariant",
                border_radius=20,
            ),


        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=10),
        padding=10,
        expand=True
    )
