import customtkinter as ctk
import tkinter as tk
import threading
import time
import ctypes
import os
import sys
from datetime import datetime
from api.roblox import get_user_id, get_limited_inventory
from api.rolimons import get_rolimons_data
from ui.theme import apply_neon_theme, enable_blur_effect
from utils.helpers import format_item_display, format_diff
from utils.storage import load_previous_data, save_current_data, ensure_user_dir
from ui.graph import show_graph
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

apply_neon_theme()

app = ctk.CTk()
app.title("Snoots Limited Tracker | V1.0.0")
app.geometry("1280x720")
app.minsize(800, 600)
app.iconbitmap(resource_path("slt.ico"))
app.wm_attributes('-transparentcolor', 'gray')

enable_blur_effect(app)

main_frame = ctk.CTkFrame(app, fg_color="gray", corner_radius=20, border_width=4, border_color="#9D00FF")
main_frame.pack(padx=30, pady=30, fill="both", expand=True)

title_label = ctk.CTkLabel(main_frame, text="Snoots Limited Tracker", font=("Roboto", 30), text_color="#9D00FF")
title_label.pack(pady=20)

status_label = ctk.CTkLabel(main_frame, text="Enter your Roblox username below:", font=("Roboto", 18), text_color="white")
status_label.pack(pady=10)

username_entry = ctk.CTkEntry(main_frame, placeholder_text="Roblox Username", width=300)
username_entry.pack(pady=10)

totals_label = ctk.CTkLabel(main_frame, text="", font=("Roboto", 18), text_color="#9D00FF")
totals_label.pack(pady=5)

last_updated_label = ctk.CTkLabel(main_frame, text="", font=("Roboto", 14), text_color="gray")
last_updated_label.pack()

limiteds_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#222222", corner_radius=10)
limiteds_frame.pack(fill="both", expand=True, padx=10, pady=10)

auto_refresh_enabled = tk.BooleanVar(value=False)
auto_refresh_delay = 60  

def refresh_limiteds():
    for widget in limiteds_frame.winfo_children():
        widget.destroy()

    username = username_entry.get()
    status_label.configure(text="Fetching data...")

    def worker():
        user_id = get_user_id(username)
        if not user_id:
            status_label.configure(text="User not found.")
            return

        inventory = get_limited_inventory(user_id)
        rolimons_data = get_rolimons_data()

        if not inventory:
            status_label.configure(text="No limiteds found or profile is private.")
            return

        total_rap = 0
        total_value = 0

        for item in inventory:
            asset_id = str(item['assetId'])
            name = item['name']
            rap = item['recentAveragePrice']
            total_rap += rap

            if asset_id in rolimons_data:
                rdata = rolimons_data[asset_id]
                value = rdata[3]
                trend = rdata[5]
            else:
                value = 0
                trend = "Unknown"

            total_value += value

            item_frame = ctk.CTkFrame(limiteds_frame, fg_color="#111111", corner_radius=10)
            item_frame.pack(pady=5, padx=10, fill="x")

            image_path = os.path.join("images", f"{asset_id}.png")
            if os.path.exists(image_path):
                try:
                    pil_image = Image.open(image_path).resize((64, 64), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(pil_image)
                    image_label = tk.Label(item_frame, image=photo, bg="#111111")
                    image_label.image = photo  
                    image_label.pack(side="left", padx=10, pady=10)
                except Exception as e:
                    print(f"Error loading image for {asset_id}: {e}")

            item_label = ctk.CTkLabel(item_frame, text=format_item_display(name, rap, value, trend),
                                      justify="left", text_color="#9D00FF", font=("Roboto", 18))
            item_label.pack(anchor="w", padx=10, pady=10)

        previous = load_previous_data()
        prev_rap = previous.get("rap", total_rap)
        prev_val = previous.get("value", total_value)

        save_current_data({"rap": total_rap, "value": total_value})

        totals_label.configure(text=f"Total RAP: {format_diff(total_rap, prev_rap)} | Value: {format_diff(total_value, prev_val)}")
        last_updated_label.configure(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        status_label.configure(text=f"Loaded {len(inventory)} limiteds for {username}")

    threading.Thread(target=worker).start()

def auto_refresh_loop():
    if auto_refresh_enabled.get():
        refresh_limiteds()
        app.after(auto_refresh_delay * 1000, auto_refresh_loop)

refresh_button = ctk.CTkButton(main_frame, text="Load Limiteds", command=refresh_limiteds,
                               text_color="#9D00FF", fg_color="black",
                               hover_color="#440066", border_width=2, border_color="#9D00FF", corner_radius=15)
refresh_button.pack(pady=10)

auto_refresh_switch = ctk.CTkSwitch(main_frame, text="Auto Refresh (1 min)", variable=auto_refresh_enabled,
                                    onvalue=True, offvalue=False, command=auto_refresh_loop)
auto_refresh_switch.pack(pady=5)

def export_data(username):
    ensure_user_dir(username)

    user_id = get_user_id(username)
    if not user_id:
        status_label.configure(text="User not found.")
        return

    status_label.configure(text=f"Data exported for {username}!")

def open_graph():
    username = username_entry.get()
    if username:
        show_graph(username)

button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=10)

export_button = ctk.CTkButton(button_frame, text="Export Data", command=lambda: export_data(username_entry.get()),
                              text_color="#9D00FF", fg_color="black",
                              hover_color="#440066", border_width=2, border_color="#9D00FF", corner_radius=15)
export_button.pack(side="left", padx=5)

graph_button = ctk.CTkButton(button_frame, text="Show Graph", command=open_graph,
                             text_color="#9D00FF", fg_color="black",
                             hover_color="#440066", border_width=2, border_color="#9D00FF", corner_radius=15)
graph_button.pack(side="left", padx=5)

app.mainloop()