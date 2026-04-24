import flet as ft
import database
import config
from views.summary import get_summary_view
from views.history import get_history_view
from views.management import get_management_view
from components.segmented_control import CustomSegmentedControl, Segment

async def main(page: ft.Page):
    page.title = "Cashew Expense Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="green", use_material3=True)
    page.padding = 0

    database.init_db()
    
    # --- FilePicker Logic (Import/Export) ---
    file_picker = ft.FilePicker()
    save_file_picker = ft.FilePicker()
    
    # Flet 0.80.2+ : On n'ajoute plus à l'overlay, on attend le résultat directement.
    # Note: On garde les instances ici pour éviter la garbage collection si nécessaire.

    async def trigger_import(e):
        # On attend le résultat directement (Pattern moderne Flet 0.80+)
        result = await file_picker.pick_files(allowed_extensions=["csv"])
        if result: # result est une liste de fichiers
            file_path = result[0].path
            success, message = database.import_from_csv(file_path)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700
            )
            page.snack_bar.open = True
            await refresh_view()
            page.update()

    async def trigger_export(e):
        path = await save_file_picker.save_file(file_name="cashew_export.csv", allowed_extensions=["csv"])
        if path:
            database.export_to_csv(path)
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Dataly voa-export tany amin'ny: {path}"))
            page.snack_bar.open = True
            page.update()

    page.trigger_import = trigger_import
    page.trigger_export = trigger_export

    # --- Consent Check ---
    async def show_consent_dialog():
        async def on_consent_change(e):
            btn_continue.disabled = not e.control.value
            page.update()

        async def on_continue(e):
            config.update_config("consent_accepted", True)
            consent_dialog.open = False
            page.update()

        btn_continue = ft.FilledButton("Manohy", disabled=True, on_click=on_continue)
        
        consent_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Fepetra fampiasana", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Vakio ny fepetra fampiasana ary mariho ny boaty raha manaiky ianao."),
                ft.Row([
                    ft.Text("Jereo ny "),
                    ft.TextButton("Conditions d'utilisation", url="https://example.com/terms"),
                ], spacing=0, wrap=True),
                ft.Checkbox(
                    label="Avy namako aho dia ekeko ny fepetra fampiasana",
                    on_change=on_consent_change
                ),
            ], tight=True, spacing=10),
            actions=[btn_continue],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(consent_dialog)
        consent_dialog.open = True
        page.update()

    if not config.is_consent_given():
        await show_consent_dialog()

    # --- Main Navigation Logic ---
    main_content = ft.Container(expand=True)

    async def navigate(e):
        index = e.control.selected_index
        if index == 0:
            main_content.content = get_summary_view(page)
        elif index == 1:
            main_content.content = get_history_view(page)
        elif index == 2:
            main_content.content = get_management_view(page)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Témoin"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Tantara"),
            ft.NavigationBarDestination(icon=ft.Icons.MORE_HORIZ, label="Fikirakirana"),
        ],
        on_change=navigate,
        selected_index=0,
    )

    # --- Add Entry Logic ---
    async def open_add_dialog(e):
        cat_flux_selector = CustomSegmentedControl(
            segments=[
                Segment(value="Miditra", label="Miditra", icon=ft.Icons.ADD),
                Segment(value="Fandaniana", label="Fandaniana", icon=ft.Icons.REMOVE),
            ],
            selected_index=1, # Default to Fandaniana
        )
        item_field = ft.TextField(label="Zavatra (Item)", autofocus=True)
        qty_field = ft.TextField(label="Isa (Quantité)", keyboard_type=ft.KeyboardType.NUMBER, expand=1)
        unit_field = ft.TextField(label="Singa (Unité : kg, lany...)", expand=1)
        price_field = ft.TextField(label="Vidy isany (Prix unitaire, Ar)", keyboard_type=ft.KeyboardType.NUMBER)
        total_field = ft.TextField(label="Totaliny (Montant total, Ar)", read_only=True, value="0")
        client_field = ft.TextField(label="Mpandray / Mpamatsy (Client / Fournisseur)")

        async def update_total(e):
            try:
                qty = float(qty_field.value) if qty_field.value else 0
                price = float(price_field.value) if price_field.value else 0
                total = qty * price
                total_field.value = f"{total:,.0f}"
                page.update()
            except ValueError:
                total_field.value = "Erreur"
                page.update()

        qty_field.on_change = update_total
        price_field.on_change = update_total
        
        async def close_dialog(e):
            dialog.open = False
            page.update()

        async def save_entry_callback(e):
            if not qty_field.value or not price_field.value or not item_field.value:
                if not qty_field.value: qty_field.error_text = "Ilaina ity"
                if not price_field.value: price_field.error_text = "Ilaina ity"
                if not item_field.value: item_field.error_text = "Ilaina ity"
                page.update()
                return
            
            try:
                q_val = float(qty_field.value)
                p_val = float(price_field.value)
                t_val = q_val * p_val
                
                f_type = cat_flux_selector.segments[cat_flux_selector.selected_index].value
                
                # Save via database module
                database.save_entry(
                    f_type, 
                    item_field.value, 
                    q_val, 
                    unit_field.value, 
                    p_val, 
                    t_val, 
                    client_field.value
                )
                
                # Feedback
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Voatahiry: {item_field.value} (Ar {t_val:,.0f})"),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
                
                # Reset UI
                item_field.value = ""
                qty_field.value = ""
                unit_field.value = ""
                price_field.value = ""
                total_field.value = "0"
                client_field.value = ""
                
                # Refresh current view
                await refresh_view()
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Nisy fahadisoana teo amin'ny isa"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Text("Ampidiro fandaniana / miditra", expand=True, size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([
                cat_flux_selector,
                item_field,
                ft.Row([qty_field, unit_field], spacing=10),
                price_field,
                total_field,
                client_field,
            ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.FilledButton("Ampidiro", on_click=save_entry_callback),
            ],
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def refresh_view():
        idx = page.navigation_bar.selected_index
        if idx == 0:
            main_content.content = get_summary_view(page)
        elif idx == 1:
            main_content.content = get_history_view(page)
        elif idx == 2:
            main_content.content = get_management_view(page)
        page.update()

    # Expose refresh_view
    page.refresh_view = refresh_view

    # --- Initial View ---
    main_content.content = get_summary_view(page)
    page.add(main_content)
    page.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.GREEN_700,
        on_click=open_add_dialog,
    )

    # --- Responsive: rebuild view on screen resize ---
    async def on_page_resize(e):
        await refresh_view()
    page.on_resize = on_page_resize

    page.update()

if __name__ == "__main__":
    import sys
    if "--web" in sys.argv:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
    else:
        ft.app(target=main, assets_dir="assets")


