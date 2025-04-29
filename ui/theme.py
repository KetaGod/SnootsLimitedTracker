import customtkinter as ctk
import ctypes
from ctypes import windll, byref, sizeof, c_int

def apply_neon_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

def enable_blur_effect(window):
    hwnd = windll.user32.GetParent(window.winfo_id())
    accent_policy = 3
    accent_struct = (accent_policy, 0, 0, 0)
    accent_pointer = ctypes.pointer((ctypes.c_int * 4)(*accent_struct))
    windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, accent_pointer, 12)
    margins = (-1, -1, -1, -1)
    windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref((ctypes.c_int * 4)(*margins)))
