# import flet as ft
# import sqlite3
# import base64
# import os

# def main(page: ft.Page):
#     page.title = "File Picker Test"
#     page.window.width = 300
#     page.window.height = 400

#     # Initialize SQLite database
#     db_path = os.path.join(os.getcwd(), "test.db")
#     db = sqlite3.connect(db_path, check_same_thread=False)
#     cursor = db.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             data BLOB
#         )
#     """)
#     db.commit()
#     print(f"Database path: {db_path}, writable: {os.access(db_path, os.W_OK)}")

#     # Function definitions
#     def handle_file_result(e: ft.FilePickerResultEvent):
#         print(f"handle_file_result called with event: {e}, files: {e.files}")
#         if e.files:
#             file = e.files[0]
#             try:
#                 global selected_file
#                 if file and hasattr(file, 'bytes'):
#                     selected_file = file
#                     image_display.src_base64 = base64.b64encode(file.bytes).decode('utf-8')
#                     status_text.value = f"Selected: {file.name} (via bytes)"
#                     save_button.disabled = False
#                 elif not page.web and hasattr(file, 'path'):
#                     selected_file = file
#                     try:
#                         with open(file.path, "rb") as f:
#                             selected_file.bytes = f.read()  # Read file content
#                         image_display.src_base64 = base64.b64encode(selected_file.bytes).decode('utf-8')
#                         status_text.value = f"Selected: {file.name} (via path)"
#                         save_button.disabled = False
#                     except PermissionError as pe:
#                         status_text.value = f"Permission denied reading {file.path}: {pe}"
#                         print(f"Permission error: {pe}")
#                     except FileNotFoundError as fnf:
#                         status_text.value = f"File not found: {file.path} - {fnf}"
#                         print(f"File not found error: {fnf}")
#                     except Exception as ex:
#                         status_text.value = f"Error reading file: {ex}"
#                         print(f"Unexpected error reading file: {ex}")
#                 else:
#                     status_text.value = "No file data available. Check permissions or Flet setup."
#                     print(f"File object details: {vars(file) if file else 'None'}")
#                     print(f"Platform: web={page.web}, path exists={hasattr(file, 'path')}, bytes exists={hasattr(file, 'bytes')}")
#             except Exception as ex:
#                 status_text.value = f"General error in file handling: {ex}"
#                 print(f"General exception: {ex}")
#         else:
#             status_text.value = "No files selected. Ensure file picker opened."
#             print("No files selected in handle_file_result")
#         page.update()

#     def pick_file(e):
#         file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)

#     def save_image(e):
#         if 'selected_file' in globals() and selected_file and hasattr(selected_file, 'bytes'):
#             cursor.execute("INSERT INTO images (name, data) VALUES (?, ?)", 
#                           (selected_file.name, selected_file.bytes))
#             db.commit()
#             status_text.value = f"Saved {selected_file.name} to database."
#             save_button.disabled = True
#             print(f"Saved image {selected_file.name} with length {len(selected_file.bytes)}")
#         else:
#             status_text.value = "No file to save or data unavailable."
#             print("No file data to save")
#         page.update()

#     # File picker and UI elements
#     file_picker = ft.FilePicker(on_result=handle_file_result)
#     image_display = ft.Image(width=200, height=200, fit="contain")
#     status_text = ft.Text("", color="red")
#     upload_button = ft.ElevatedButton("Upload/Select Image", icon=ft.Icons.IMAGE, on_click=pick_file, disabled=False)
#     save_button = ft.ElevatedButton("Save Image", on_click=save_image, disabled=True)

#     # Add controls to page
#     page.overlay.append(file_picker)
#     page.add(
#         upload_button,
#         image_display,
#         status_text,
#         save_button
#     )

# ft.app(target=main)


import flet as ft
import sqlite3
import base64
import os
import time

def main(page: ft.Page):
    page.title = "File Picker Test"
    page.window.width = 300
    page.window.height = 400

    # Initialize SQLite database
    db_path = os.path.join(os.getcwd(), "test.db")
    db = sqlite3.connect(db_path, check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            data BLOB
        )
    """)
    db.commit()
    print(f"Database path: {db_path}, writable: {os.access(db_path, os.W_OK)}")

    # Function definitions
    def handle_file_result(e: ft.FilePickerResultEvent, cursor, db):
        print(f"handle_file_result called with event: {e}, files: {e.files}")
        if e.files:
            file = e.files[0]
            try:
                global selected_file
                if file and hasattr(file, 'bytes'):
                    selected_file = file
                    image_display.src_base64 = base64.b64encode(file.bytes).decode('utf-8')
                    status_text.value = f"Selected: {file.name} (via bytes), bytes length: {len(file.bytes)}"
                    save_button.disabled = False
                elif not page.web and hasattr(file, 'path'):
                    selected_file = file
                    try:
                        with open(file.path, "rb") as f:
                            selected_file.bytes = f.read()  # Read file content
                        # Debug: Write to a temp file to verify data
                        temp_path = os.path.join(os.getcwd(), "temp_debug.jpg")
                        with open(temp_path, "wb") as temp_f:
                            temp_f.write(selected_file.bytes)
                        image_display.src_base64 = base64.b64encode(selected_file.bytes).decode('utf-8')
                        status_text.value = f"Selected: {file.name} (via path), bytes length: {len(selected_file.bytes)}"
                        save_button.disabled = False
                        print(f"Debug: Wrote {len(selected_file.bytes)} bytes to {temp_path}")
                    except PermissionError as pe:
                        status_text.value = f"Permission denied reading {file.path}: {pe}"
                        print(f"Permission error: {pe}")
                    except FileNotFoundError as fnf:
                        status_text.value = f"File not found: {file.path} - {fnf}"
                        print(f"File not found error: {fnf}")
                    except Exception as ex:
                        status_text.value = f"Error reading file: {ex}"
                        print(f"Unexpected error reading file: {ex}")
                else:
                    status_text.value = "No file data available. Check permissions or Flet setup."
                    print(f"File object details: {vars(file) if file else 'None'}")
                    print(f"Platform: web={page.web}, path exists={hasattr(file, 'path')}, bytes exists={hasattr(file, 'bytes')}")
            except Exception as ex:
                status_text.value = f"General error in file handling: {ex}"
                print(f"General exception: {ex}")
        else:
            status_text.value = "No files selected. Ensure file picker opened."
            print("No files selected in handle_file_result")
        page.update()

    def pick_file(e, file_picker, cursor, db):
        file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)

    def save_image(e, cursor, db):
        if 'selected_file' in globals() and selected_file and hasattr(selected_file, 'bytes'):
            bytes_length = len(selected_file.bytes)
            print(f"Attempting to save {selected_file.name} with {bytes_length} bytes")
            cursor.execute("INSERT INTO images (name, data) VALUES (?, ?)", 
                          (selected_file.name, selected_file.bytes))
            db.commit()
            db.execute("PRAGMA wal_checkpoint(FULL)")  # Force flush to disk
            print(f"Commit successful, rowcount: {cursor.rowcount}, lastrowid: {cursor.lastrowid}")
            # Verify data in database
            cursor.execute("SELECT length(data) FROM images WHERE id = ?", (cursor.lastrowid,))
            stored_length = cursor.fetchone()[0]
            print(f"Verified length in database: {stored_length}")
            # Add a small delay to ensure flush
            time.sleep(0.1)
        else:
            status_text.value = "No file to save or data unavailable."
            print(f"Save failed: selected_file={selected_file}, bytes exists={hasattr(selected_file, 'bytes') if 'selected_file' in globals() else 'None'}")
        page.update()

    # File picker and UI elements
    file_picker = ft.FilePicker(on_result=lambda e: handle_file_result(e, cursor, db))
    image_display = ft.Image(width=200, height=200, fit="contain")
    status_text = ft.Text("", color="red")
    upload_button = ft.ElevatedButton("Upload/Select Image", icon=ft.Icons.IMAGE, on_click=lambda e: pick_file(e, file_picker, cursor, db), disabled=False)
    save_button = ft.ElevatedButton("Save Image", on_click=lambda e: save_image(e, cursor, db), disabled=True)

    # Add controls to page
    page.overlay.append(file_picker)
    page.add(
        upload_button,
        image_display,
        status_text,
        save_button
    )

ft.app(target=main)