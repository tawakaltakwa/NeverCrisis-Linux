#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
FINAL FANTASY VII EVER CRISIS - Server Args Manager & Offline Launcher
==============================================================================
Aplikasi GUI Modern berbasis Tkinter untuk:
1. Membaca, menampilkan, dan mengedit file server_args.txt secara langsung.
2. Menyediakan pop-up bantuan untuk memilih & menambahkan item dari folder items/
   dengan nilai kustom (custom value / count).
3. Tombol Reset untuk mengosongkan editor (dengan konfirmasi).
4. Menjalankan start_offline.sh di Terminal (Kitty/Alacritty).
5. Template preset instan (Starter Pack, Unlock All, Cloud OB10, Reset Account).
==============================================================================
"""

import os
import sys
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Direktori & File Konfigurasi
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_ARGS_PATH = os.path.join(SCRIPT_DIR, "server_args.txt")
START_SCRIPT_PATH = os.path.join(SCRIPT_DIR, "start_offline.sh")
ITEMS_DIR = os.path.join(SCRIPT_DIR, "items")
TIFA_IMG_PATH = os.path.join(SCRIPT_DIR, "latar-tifa.png")

# Palet Warna Tema Modern Dark (Catppuccin Mocha Inspired)
THEME = {
    "bg_dark": "#181825",
    "bg_card": "#1e1e2e",
    "bg_surface": "#252538",
    "bg_input": "#313244",
    "bg_hover": "#45475a",
    "border": "#363a4f",
    "border_focus": "#89b4fa",
    "text_main": "#cdd6f4",
    "text_muted": "#a6adc8",
    "text_dim": "#6c7086",
    "accent_cyan": "#00d4ff",
    "accent_blue": "#89b4fa",
    "accent_green": "#a6e3a1",
    "accent_yellow": "#f9e2af",
    "accent_red": "#f38ba8",
    "accent_purple": "#cba6f7",
    "selection": "#45475a",
    "highlight_comment": "#6c7086",
    "highlight_give": "#89b4fa",
    "highlight_reset": "#f38ba8"
}

# Shortcut Mata Uang / Currencies Bawaan Server (Tanpa perlu ID file)
CURRENCIES = [
    {"id": "crystals", "name": "Blue Crystals (Permata Biru Gratis)", "cat": "Mata Uang (Currencies)", "default": 50000, "cmd": "--give crystals={count}"},
    {"id": "red_crystals", "name": "Red Crystals (Permata Merah Berbayar)", "cat": "Mata Uang (Currencies)", "default": 10000, "cmd": "--give red_crystals={count}"},
    {"id": "gil", "name": "Gil (Mata Uang Utama)", "cat": "Mata Uang (Currencies)", "default": 500000000, "cmd": "--give gil={count}"},
    {"id": "stamina", "name": "Stamina", "cat": "Mata Uang (Currencies)", "default": 999, "cmd": "--give stamina={count}"},
    {"id": "chocobo_medals", "name": "Chocobo Medals", "cat": "Mata Uang (Currencies)", "default": 50000, "cmd": "--give chocobo_medals={count}"},
    {"id": "weapon_medals", "name": "Weapon Medals", "cat": "Mata Uang (Currencies)", "default": 50000, "cmd": "--give weapon_medals={count}"},
    {"id": "crisis_medals", "name": "Crisis Medals", "cat": "Mata Uang (Currencies)", "default": 50000, "cmd": "--give crisis_medals={count}"},
    {"id": "dungeon_keys", "name": "Dungeon Keys", "cat": "Mata Uang (Currencies)", "default": 50, "cmd": "--give dungeon_keys={count}"},
    {"id": "gear_vouchers", "name": "Gear Vouchers", "cat": "Mata Uang (Currencies)", "default": 10, "cmd": "--give gear_vouchers={count}"},
    {"id": "memory_vouchers", "name": "Memory Vouchers", "cat": "Mata Uang (Currencies)", "default": 20, "cmd": "--give memory_vouchers={count}"},
    {"id": "parts", "name": "Weapon Parts Umum", "cat": "Mata Uang (Currencies)", "default": 1000, "cmd": "--give parts={count}"},
]

CHARACTERS = [
    "Semua Karakter", "Cloud", "Tifa", "Aerith", "Barret", "Zack",
    "Sephiroth", "Sephiroth (Original)", "Yuffie", "Cait Sith",
    "Vincent", "Cid", "Glenn", "Matt", "Lucia", "Angeal", "Red XIII"
]


class ItemDatabase:
    """Memuat dan mengelola seluruh database item dari direktori items/"""
    def __init__(self, items_dir):
        self.items_dir = items_dir
        self.items = []
        self.categories = set()
        self.load_all()

    def load_all(self):
        self.items = []
        self.categories = set()

        # 1. Tambahkan mata uang bawaan (Shortcut tanpa ID)
        for c in CURRENCIES:
            self.items.append({
                "id": c["id"],
                "name": c["name"],
                "category": c["cat"],
                "detail": "Shortcut Currency",
                "character": "Umum",
                "type": "currency",
                "default_val": c["default"],
                "cmd_template": c["cmd"]
            })
        self.categories.add("Mata Uang (Currencies)")

        # 2. Tambahkan Perintah Khusus / Flags
        special_cmds = [
            {"id": "--reset-account", "name": "Reset Seluruh Akun Server ke Baru", "category": "Perintah Khusus", "detail": "Flag Reset", "character": "Umum", "type": "special", "default_val": 1, "cmd_template": "--reset-account"},
            {"id": "costume=all", "name": "Buka SEMUA Kostum Semua Karakter", "category": "Perintah Khusus", "detail": "Unlock All", "character": "Semua", "type": "special", "default_val": 1, "cmd_template": "--give costume=all"},
            {"id": "wallpaper=all", "name": "Buka SEMUA Wallpaper Home Screen", "category": "Perintah Khusus", "detail": "Unlock All", "character": "Semua", "type": "special", "default_val": 1, "cmd_template": "--give wallpaper=all"},
            {"id": "memoria=all", "name": "Buka SEMUA Memoria", "category": "Perintah Khusus", "detail": "Unlock All", "character": "Semua", "type": "special", "default_val": 1, "cmd_template": "--give memoria=all"},
        ]
        for s in special_cmds:
            self.items.append(s)
        self.categories.add("Perintah Khusus")

        # 3. Baca seluruh file txt di folder items/
        file_category_map = {
            "weapons.txt": ("Senjata (Weapons)", "weapon"),
            "costumes.txt": ("Kostum (Costumes)", "costume"),
            "materials.txt": ("Material Upgrade", "item"),
            "weapon-parts.txt": ("Weapon Parts", "item"),
            "tickets-medals-events.txt": ("Tiket & Medali Event", "item"),
            "chocobo.txt": ("Chocobo Expedition", "item"),
            "wallpapers.txt": ("Wallpapers", "wallpaper"),
            "memoria.txt": ("Memoria", "memoria"),
            "misc.txt": ("Item Lainnya (Misc)", "item")
        }

        for filename, (cat_name, item_type) in file_category_map.items():
            path = os.path.join(self.items_dir, filename)
            if not os.path.exists(path):
                continue

            self.categories.add(cat_name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or line.startswith("id\t"):
                            continue
                        parts = line.split("\t")
                        if not parts:
                            continue

                        item_id = parts[0].strip()

                        if item_type == "weapon":
                            rarity = parts[1].strip() if len(parts) > 1 else "SSR"
                            name = parts[2].strip() if len(parts) > 2 else f"Weapon {item_id}"
                            char = parts[3].strip()
                            self.items.append({
                                "id": item_id,
                                "name": name,
                                "category": cat_name,
                                "detail": f"Rarity: {rarity}",
                                "character": char,
                                "type": "weapon",
                                "default_val": 11,  # 11 = Max rarity + OB10 Overboost
                                "cmd_template": "--give weapon={id}={count}"
                            })

                        elif item_type == "costume":
                            char = parts[1].strip() if len(parts) > 1 else "Unknown"
                            name = parts[2].strip() if len(parts) > 2 else f"Costume {item_id}"
                            self.items.append({
                                "id": item_id,
                                "name": name,
                                "category": cat_name,
                                "detail": f"Karakter: {char}",
                                "character": char,
                                "type": "costume",
                                "default_val": 1,
                                "cmd_template": "--give costume={id}"
                            })

                        elif item_type == "wallpaper":
                            name = parts[1].strip() if len(parts) > 1 else f"Wallpaper {item_id}"
                            self.items.append({
                                "id": item_id,
                                "name": name,
                                "category": cat_name,
                                "detail": "Wallpaper",
                                "character": "Umum",
                                "type": "wallpaper",
                                "default_val": 1,
                                "cmd_template": "--give wallpaper={id}"
                            })

                        elif item_type == "memoria":
                            name = parts[1].strip() if len(parts) > 1 else f"Memoria {item_id}"
                            self.items.append({
                                "id": item_id,
                                "name": name,
                                "category": cat_name,
                                "detail": "Memoria",
                                "character": "Umum",
                                "type": "memoria",
                                "default_val": 1,
                                "cmd_template": "--give memoria={id}"
                            })

                        else:  # item types: materials, parts, tickets, etc.
                            name = parts[1].strip() if len(parts) > 1 else f"Item {item_id}"
                            char_found = "Umum"
                            for ch in CHARACTERS[1:]:
                                if ch.lower() in name.lower():
                                    char_found = ch
                                    break

                            self.items.append({
                                "id": item_id,
                                "name": name,
                                "category": cat_name,
                                "detail": f"ID: {item_id}",
                                "character": char_found,
                                "type": "item",
                                "default_val": 1000,
                                "cmd_template": "--give item={id}={count}"
                            })

            except Exception as e:
                print(f"Error membaca {filename}: {e}", file=sys.stderr)


class ItemHelperDialog(tk.Toplevel):
    """Pop-up Bantuan untuk mencari & menambahkan item dari folder items/"""
    def __init__(self, parent, db: ItemDatabase, on_add_callback):
        super().__init__(parent)
        self.title("✨ Bantuan Pemilih Item - FF7 Ever Crisis")
        self.geometry("980x720")
        self.minsize(820, 600)
        self.configure(bg=THEME["bg_dark"])

        self.db = db
        self.on_add_callback = on_add_callback
        self.filtered_items = []
        self.selected_item = None

        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.apply_filter()

        # Posisi jendela di tengah induk
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        self.geometry(f"+{px + max(0, (pw - w) // 2)}+{py + max(0, (ph - h) // 2)}")

    def setup_ui(self):
        # 1. Header Frame
        header = tk.Frame(self, bg=THEME["bg_card"], padx=16, pady=12, highlightthickness=1, highlightbackground=THEME["border"])
        header.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header,
            text="✨ Bantuan Pemilih Item & Nilai Kustom",
            font=("DejaVu Sans", 13, "bold"),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card"]
        )
        title_lbl.pack(anchor=tk.W)

        desc_lbl = tk.Label(
            header,
            text="Pilih item dari database (folder items/), tentukan jumlah (count), lalu klik 'Tambahkan'. Anda dapat menambahkan beberapa item sekaligus tanpa menutup pop-up.",
            font=("DejaVu Sans", 9),
            fg=THEME["text_muted"],
            bg=THEME["bg_card"]
        )
        desc_lbl.pack(anchor=tk.W, pady=(2, 0))

        # 2. Filter Bar
        filter_frame = tk.Frame(self, bg=THEME["bg_surface"], padx=14, pady=10, highlightthickness=1, highlightbackground=THEME["border"])
        filter_frame.pack(fill=tk.X, padx=12, pady=(10, 0))

        # Kategori
        tk.Label(filter_frame, text="Kategori:", fg=THEME["text_main"], bg=THEME["bg_surface"], font=("DejaVu Sans", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 6))

        cats = ["Semua Kategori"] + sorted(list(self.db.categories))
        self.cat_var = tk.StringVar(value="Semua Kategori")
        cat_combo = ttk.Combobox(filter_frame, textvariable=self.cat_var, values=cats, state="readonly", width=23)
        cat_combo.grid(row=0, column=1, padx=(0, 14), pady=2)
        cat_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        # Karakter
        tk.Label(filter_frame, text="Karakter:", fg=THEME["text_main"], bg=THEME["bg_surface"], font=("DejaVu Sans", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(0, 6))

        self.char_var = tk.StringVar(value="Semua Karakter")
        char_combo = ttk.Combobox(filter_frame, textvariable=self.char_var, values=CHARACTERS, state="readonly", width=18)
        char_combo.grid(row=0, column=3, padx=(0, 14), pady=2)
        char_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        # Cari Teks
        tk.Label(filter_frame, text="🔍 Cari (ID / Nama):", fg=THEME["text_main"], bg=THEME["bg_surface"], font=("DejaVu Sans", 9, "bold")).grid(row=0, column=4, sticky=tk.W, padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bg=THEME["bg_input"],
            fg=THEME["text_main"],
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT,
            font=("DejaVu Sans", 10),
            width=20
        )
        self.search_entry.grid(row=0, column=5, padx=(0, 6), pady=2, ipady=3)
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        btn_clear = tk.Button(
            filter_frame,
            text="✕",
            command=self.clear_search,
            bg=THEME["bg_input"],
            fg=THEME["text_muted"],
            activebackground=THEME["bg_hover"],
            activeforeground=THEME["text_main"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=6
        )
        btn_clear.grid(row=0, column=6)

        # 3. Status Bar Count
        self.count_lbl = tk.Label(
            self,
            text="Memuat item...",
            fg=THEME["text_dim"],
            bg=THEME["bg_dark"],
            font=("DejaVu Sans", 8)
        )
        self.count_lbl.pack(anchor=tk.W, padx=16, pady=(6, 2))

        # 4. Tabel / Treeview
        table_frame = tk.Frame(self, bg=THEME["bg_dark"], padx=12, pady=0)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "category", "detail", "character")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID / Kode")
        self.tree.heading("name", text="Nama Item")
        self.tree.heading("category", text="Kategori")
        self.tree.heading("detail", text="Detail / Rarity")
        self.tree.heading("character", text="Karakter Terkait")

        self.tree.column("id", width=120, anchor=tk.W)
        self.tree.column("name", width=340, anchor=tk.W)
        self.tree.column("category", width=170, anchor=tk.W)
        self.tree.column("detail", width=140, anchor=tk.W)
        self.tree.column("character", width=130, anchor=tk.W)

        tree_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)
        self.tree.bind("<Double-1>", lambda e: self.do_add(append=True))
        self.tree.bind("<Return>", lambda e: self.do_add(append=True))

        # 5. Konfigurasi Item & Nilai Kustom
        cfg_frame = tk.Frame(self, bg=THEME["bg_surface"], padx=16, pady=10, highlightthickness=1, highlightbackground=THEME["border"])
        cfg_frame.pack(fill=tk.X, padx=12, pady=10)

        # Baris Info Item Terpilih
        self.selected_lbl = tk.Label(
            cfg_frame,
            text="Pilih item dari tabel di atas...",
            font=("DejaVu Sans", 10, "bold"),
            fg=THEME["accent_yellow"],
            bg=THEME["bg_surface"],
            anchor=tk.W
        )
        self.selected_lbl.pack(fill=tk.X, pady=(0, 6))

        # Baris Input Nilai
        val_row = tk.Frame(cfg_frame, bg=THEME["bg_surface"])
        val_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(val_row, text="Jumlah / Nilai Kustom:", font=("DejaVu Sans", 9, "bold"), fg=THEME["text_main"], bg=THEME["bg_surface"]).pack(side=tk.LEFT, padx=(0, 8))

        self.val_var = tk.StringVar(value="1000")
        self.val_entry = tk.Entry(
            val_row,
            textvariable=self.val_var,
            font=("DejaVu Sans Mono", 10, "bold"),
            bg=THEME["bg_input"],
            fg=THEME["accent_cyan"],
            insertbackground=THEME["accent_cyan"],
            width=16,
            relief=tk.FLAT
        )
        self.val_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        self.val_var.trace_add("write", lambda *args: self.update_preview())

        # Tombol Preset Nilai Cepat
        tk.Label(val_row, text="Preset:", font=("DejaVu Sans", 8), fg=THEME["text_dim"], bg=THEME["bg_surface"]).pack(side=tk.LEFT, padx=(0, 4))
        presets = [("1", 1), ("10", 10), ("100", 100), ("1.000", 1000), ("5.000", 5000), ("11 (OB10 Max)", 11), ("10.000", 10000), ("500 Juta", 500000000)]
        for label, pval in presets:
            btn = tk.Button(
                val_row,
                text=label,
                command=lambda v=pval: self.set_preset_val(v),
                bg=THEME["bg_input"],
                fg=THEME["text_main"],
                activebackground=THEME["bg_hover"],
                activeforeground=THEME["text_main"],
                font=("DejaVu Sans", 8),
                relief=tk.FLAT,
                cursor="hand2",
                padx=5,
                pady=1
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Opsi Checkbox & Live Preview
        opts_row = tk.Frame(cfg_frame, bg=THEME["bg_surface"])
        opts_row.pack(fill=tk.X, pady=(2, 6))

        self.comment_var = tk.BooleanVar(value=True)
        cb_comment = tk.Checkbutton(
            opts_row,
            text="Sertakan komentar nama item (# Nama)",
            variable=self.comment_var,
            bg=THEME["bg_surface"],
            fg=THEME["text_main"],
            selectcolor=THEME["bg_input"],
            activebackground=THEME["bg_surface"],
            activeforeground=THEME["text_main"],
            font=("DejaVu Sans", 8),
            command=self.update_preview
        )
        cb_comment.pack(side=tk.LEFT, padx=(0, 16))

        # Live Preview Box
        preview_box = tk.Frame(cfg_frame, bg=THEME["bg_input"], padx=10, pady=6, highlightthickness=1, highlightbackground=THEME["border"])
        preview_box.pack(fill=tk.X, pady=(2, 4))

        tk.Label(preview_box, text="Preview Perintah Server:", font=("DejaVu Sans", 8, "bold"), fg=THEME["text_dim"], bg=THEME["bg_input"]).pack(anchor=tk.W)
        self.preview_lbl = tk.Label(
            preview_box,
            text="--",
            font=("DejaVu Sans Mono", 10, "bold"),
            fg=THEME["accent_green"],
            bg=THEME["bg_input"],
            anchor=tk.W,
            justify=tk.LEFT
        )
        self.preview_lbl.pack(fill=tk.X, pady=(2, 0))

        # 6. Action Buttons Bar & Toast Notification
        act_row = tk.Frame(self, bg=THEME["bg_dark"], padx=14, pady=10)
        act_row.pack(fill=tk.X, side=tk.BOTTOM)

        self.toast_lbl = tk.Label(
            act_row,
            text="",
            font=("DejaVu Sans", 9, "bold"),
            fg=THEME["accent_green"],
            bg=THEME["bg_dark"],
            anchor=tk.W
        )
        self.toast_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_add_append = tk.Button(
            act_row,
            text="➕ Tambahkan ke Akhir",
            command=lambda: self.do_add(append=True),
            bg="#2e7d32",
            fg="#ffffff",
            activebackground="#388e3c",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=6
        )
        btn_add_append.pack(side=tk.RIGHT, padx=(6, 0))

        btn_add_cursor = tk.Button(
            act_row,
            text="📍 Sisipkan di Kursor",
            command=lambda: self.do_add(append=False),
            bg="#1565c0",
            fg="#ffffff",
            activebackground="#1976d2",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_add_cursor.pack(side=tk.RIGHT, padx=(6, 0))

        btn_close = tk.Button(
            act_row,
            text="Tutup",
            command=self.destroy,
            bg=THEME["bg_surface"],
            fg=THEME["text_muted"],
            activebackground=THEME["bg_hover"],
            activeforeground=THEME["text_main"],
            font=("DejaVu Sans", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_close.pack(side=tk.RIGHT)

    def clear_search(self):
        self.search_var.set("")
        self.apply_filter()

    def set_preset_val(self, val):
        self.val_var.set(str(val))
        self.update_preview()

    def apply_filter(self):
        cat = self.cat_var.get()
        char = self.char_var.get()
        q = self.search_var.get().strip().lower()

        # Bersihkan treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.filtered_items = []
        for it in self.db.items:
            # Filter Kategori
            if cat != "Semua Kategori" and it["category"] != cat:
                continue

            # Filter Karakter
            if char != "Semua Karakter":
                if it["character"] != char and char.lower() not in it["name"].lower():
                    continue

            # Filter Pencarian Teks
            if q:
                match_id = q in str(it["id"]).lower()
                match_name = q in it["name"].lower()
                match_detail = q in it.get("detail", "").lower()
                if not (match_id or match_name or match_detail):
                    continue

            self.filtered_items.append(it)

        # Masukkan ke treeview (limit 1000 untuk performa maksimal)
        limit = 1000
        for it in self.filtered_items[:limit]:
            self.tree.insert("", tk.END, values=(
                it["id"],
                it["name"],
                it["category"],
                it.get("detail", ""),
                it.get("character", "")
            ))

        total_txt = f"Menampilkan {min(len(self.filtered_items), limit)} dari {len(self.filtered_items)} item cocok (Total database: {len(self.db.items)} item)"
        self.count_lbl.config(text=total_txt)

        # Pilih item pertama jika ada
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.on_select_item(None)

    def on_select_item(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        if not vals:
            return

        item_id = str(vals[0])
        found = None
        for it in self.filtered_items:
            if str(it["id"]) == item_id:
                found = it
                break

        if not found:
            return

        self.selected_item = found
        self.selected_lbl.config(
            text=f"Terpilih: [{found['id']}] {found['name']}  ({found['category']} • {found.get('detail', '')})"
        )

        cur_val = self.val_var.get().strip()
        if not cur_val or cur_val in ("1", "10", "11", "1000", "50000", "500000000"):
            self.val_var.set(str(found.get("default_val", 1000)))

        self.update_preview()

    def generate_command_line(self):
        if not self.selected_item:
            return ""

        it = self.selected_item
        itype = it["type"]
        val_str = self.val_var.get().strip() or "1"
        try:
            val_num = int(val_str)
        except ValueError:
            val_num = 1

        cmd_line = ""

        if itype == "currency":
            cmd_line = f"--give {it['id']}={val_num}"

        elif itype == "weapon":
            # Jika 1 kopi: --give weapon=ID, jika >1: --give weapon=ID=COUNT
            if val_num <= 1:
                cmd_line = f"--give weapon={it['id']}"
            else:
                cmd_line = f"--give weapon={it['id']}={val_num}"

        elif itype == "costume":
            cmd_line = f"--give costume={it['id']}"

        elif itype == "wallpaper":
            cmd_line = f"--give wallpaper={it['id']}"

        elif itype == "memoria":
            cmd_line = f"--give memoria={it['id']}"

        elif itype == "special":
            cmd_line = it["cmd_template"]

        else:  # item (materials, parts, tickets, etc.)
            cmd_line = f"--give item={it['id']}={val_num}"

        lines = []
        if self.comment_var.get():
            lines.append(f"# {it['name']}")
        lines.append(cmd_line)

        return "\n".join(lines)

    def update_preview(self):
        text = self.generate_command_line()
        if text:
            self.preview_lbl.config(text=text)
        else:
            self.preview_lbl.config(text="-- (Belum ada item terpilih) --")

    def do_add(self, append=True):
        entry_text = self.generate_command_line()
        if not entry_text:
            return

        self.on_add_callback(entry_text, append=append)

        # Toast badge
        it_name = self.selected_item['name'] if self.selected_item else "Item"
        self.toast_lbl.config(
            text=f"✅ Berhasil ditambahkan: {it_name}!",
            fg=THEME["accent_green"]
        )
        self.after(3000, lambda: self.toast_lbl.config(text=""))


class ArgsEditorApp(tk.Tk):
    """Aplikasi Utama GUI Editor server_args.txt & Launcher"""
    def __init__(self):
        super().__init__()
        self.title("FF7 Ever Crisis - Server Args Editor & Offline Launcher")
        self.geometry("1020x750")
        self.minsize(820, 580)
        self.configure(bg=THEME["bg_dark"])

        self.file_path = SERVER_ARGS_PATH
        self.is_modified = False
        self.suppress_modified_event = False

        # Database Item dari folder items/
        self.db = ItemDatabase(ITEMS_DIR)

        # Inisialisasi Tampilan
        self.setup_styles()
        self.setup_ui()
        self.load_file()
        self.setup_shortcuts()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Konfigurasi Treeview
        style.configure(
            "Treeview",
            background=THEME["bg_card"],
            foreground=THEME["text_main"],
            fieldbackground=THEME["bg_card"],
            rowheight=26,
            font=("DejaVu Sans", 9),
            borderwidth=0
        )
        style.map(
            "Treeview",
            background=[("selected", THEME["selection"])],
            foreground=[("selected", THEME["accent_cyan"])]
        )
        style.configure(
            "Treeview.Heading",
            background=THEME["bg_surface"],
            foreground=THEME["text_main"],
            font=("DejaVu Sans", 9, "bold"),
            relief="flat",
            padding=4
        )
        style.map("Treeview.Heading", background=[("active", THEME["bg_hover"])])

        # Combobox
        style.configure(
            "TCombobox",
            fieldbackground=THEME["bg_input"],
            background=THEME["bg_surface"],
            foreground=THEME["text_main"],
            arrowcolor=THEME["accent_cyan"],
            relief="flat",
            padding=3
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", THEME["bg_input"])],
            selectbackground=[("readonly", THEME["bg_input"])],
            selectforeground=[("readonly", THEME["text_main"])]
        )

        # Scrollbars
        style.configure(
            "Vertical.TScrollbar",
            background=THEME["bg_surface"],
            troughcolor=THEME["bg_dark"],
            bordercolor=THEME["bg_dark"],
            arrowcolor=THEME["text_muted"],
            relief="flat"
        )
        style.configure(
            "Horizontal.TScrollbar",
            background=THEME["bg_surface"],
            troughcolor=THEME["bg_dark"],
            bordercolor=THEME["bg_dark"],
            arrowcolor=THEME["text_muted"],
            relief="flat"
        )

    def setup_ui(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=THEME["bg_card"], padx=18, pady=8, highlightthickness=1, highlightbackground=THEME["border"])
        header.pack(fill=tk.X, side=tk.TOP)

        # Bagian Kiri: title_lbl, sub_lbl, status_box
        left_header = tk.Frame(header, bg=THEME["bg_card"])
        left_header.pack(side=tk.LEFT, fill=tk.Y)

        title_lbl = tk.Label(
            left_header,
            text="⚔️ FINAL FANTASY VII EVER CRISIS",
            font=("DejaVu Sans", 14, "bold"),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card"]
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            left_header,
            text="Editor Argumen Server Offline (server_args.txt) & Peluncur Game",
            font=("DejaVu Sans", 9),
            fg=THEME["text_muted"],
            bg=THEME["bg_card"]
        )
        sub_lbl.pack(anchor=tk.W, pady=(4, 0))

        # Status box di bawah title & subtitle pada sisi kiri
        status_box = tk.Frame(left_header, bg=THEME["bg_card"])
        status_box.pack(anchor=tk.SW, pady=(10, 0), side=tk.BOTTOM)

        self.file_info_lbl = tk.Label(
            status_box,
            text="server_args.txt",
            font=("DejaVu Sans Mono", 9),
            fg=THEME["text_muted"],
            bg=THEME["bg_card"]
        )
        self.file_info_lbl.pack(side=tk.LEFT)

        sep_status = tk.Label(status_box, text=" | ", font=("DejaVu Sans", 9), fg=THEME["border"], bg=THEME["bg_card"])
        sep_status.pack(side=tk.LEFT)

        self.save_status_badge = tk.Label(
            status_box,
            text="● Tersimpan",
            font=("DejaVu Sans", 9, "bold"),
            fg=THEME["accent_green"],
            bg=THEME["bg_card"]
        )
        self.save_status_badge.pack(side=tk.LEFT)

        # Bagian Kanan: Gambar Tifa (tifa_photo)
        self.tifa_photo = None
        if os.path.exists(TIFA_IMG_PATH):
            try:
                if HAS_PIL:
                    img = Image.open(TIFA_IMG_PATH)
                    target_h = 200
                    target_w = int(img.width * (target_h / img.height))
                    img_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    self.tifa_photo = ImageTk.PhotoImage(img_resized)
                else:
                    self.tifa_photo = tk.PhotoImage(file=TIFA_IMG_PATH).subsample(3, 3)

                tifa_lbl = tk.Label(
                    header,
                    image=self.tifa_photo,
                    bg=THEME["bg_card"],
                    borderwidth=0,
                    highlightthickness=0
                )
                tifa_lbl.pack(side=tk.RIGHT)
            except Exception as e:
                print(f"Error memuat latar-tifa.png: {e}", file=sys.stderr)

        # 2. Main Action Toolbar
        toolbar = tk.Frame(self, bg=THEME["bg_surface"], padx=14, pady=8, highlightthickness=1, highlightbackground=THEME["border"])
        toolbar.pack(fill=tk.X, side=tk.TOP)

        # Tombol Simpan
        self.btn_save = tk.Button(
            toolbar,
            text="💾 Simpan (Ctrl+S)",
            command=self.save_file,
            bg="#1e88e5",
            fg="#ffffff",
            activebackground="#1976d2",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6
        )
        self.btn_save.pack(side=tk.LEFT, padx=(0, 6))

        # Tombol Buka Ulang
        btn_reload = tk.Button(
            toolbar,
            text="🔄 Buka Ulang",
            command=self.reload_file,
            bg=THEME["bg_input"],
            fg=THEME["text_main"],
            activebackground=THEME["bg_hover"],
            activeforeground=THEME["text_main"],
            font=("DejaVu Sans", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=6
        )
        btn_reload.pack(side=tk.LEFT, padx=(0, 10))

        # Separator visual
        sep1 = tk.Frame(toolbar, width=2, bg=THEME["border"], height=24)
        sep1.pack(side=tk.LEFT, padx=(0, 10))

        # TOMBOL UTAMA: Bantuan Item Pop-up
        btn_helper = tk.Button(
            toolbar,
            text="✨ Bantuan Tambah Item",
            command=self.open_item_helper,
            bg="#6a1b9a",
            fg="#ffffff",
            activebackground="#7b1fa2",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=6
        )
        btn_helper.pack(side=tk.LEFT, padx=(0, 10))

        # TOMBOL UTAMA: Reset untuk mengosongkan
        btn_reset = tk.Button(
            toolbar,
            text="🗑️ Reset",
            command=self.reset_content,
            bg="#c62828",
            fg="#ffffff",
            activebackground="#d32f2f",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_reset.pack(side=tk.LEFT, padx=(0, 10))

        # Dropdown Template / Presets
        btn_presets = tk.Menubutton(
            toolbar,
            text="📋 Preset Rekomendasi ▼",
            bg=THEME["bg_input"],
            fg=THEME["text_main"],
            activebackground=THEME["bg_hover"],
            activeforeground=THEME["text_main"],
            font=("DejaVu Sans", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=6
        )
        preset_menu = tk.Menu(btn_presets, tearoff=0, bg=THEME["bg_card"], fg=THEME["text_main"], activebackground=THEME["selection"], activeforeground=THEME["accent_cyan"], font=("DejaVu Sans", 9))
        preset_menu.add_command(label="🌟 Starter Pack Kaya (500M Gil + 50k Crystals + Stamina)", command=self.apply_preset_starter)
        preset_menu.add_command(label="👕 Buka Seluruh Kostum, Wallpaper & Memoria", command=self.apply_preset_all_unlocks)
        preset_menu.add_command(label="🔄 Reset Akun Server Baru (--reset-account)", command=self.apply_preset_reset_account)
        btn_presets.configure(menu=preset_menu)
        btn_presets.pack(side=tk.LEFT, padx=(0, 10))

        # TOMBOL UTAMA KANAN: Jalankan start_offline.sh di Terminal
        btn_term_run = tk.Button(
            toolbar,
            text="🚀 Simpan & Jalankan",
            command=self.run_server_in_terminal,
            bg="#2e7d32",
            fg="#ffffff",
            activebackground="#388e3c",
            activeforeground="#ffffff",
            font=("DejaVu Sans", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=6
        )
        btn_term_run.pack(side=tk.RIGHT)

        # 3. Bar Pencarian Teks Editor (Ctrl+F)
        self.find_frame = tk.Frame(self, bg=THEME["bg_surface"], padx=14, pady=6, highlightthickness=1, highlightbackground=THEME["border"])
        # Tidak dipack langsung, dipack saat Ctrl+F ditekan

        tk.Label(self.find_frame, text="🔍 Cari di Editor:", fg=THEME["text_main"], bg=THEME["bg_surface"], font=("DejaVu Sans", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        self.find_var = tk.StringVar()
        self.find_entry = tk.Entry(
            self.find_frame,
            textvariable=self.find_var,
            bg=THEME["bg_input"],
            fg=THEME["text_main"],
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT,
            font=("DejaVu Sans", 9),
            width=26
        )
        self.find_entry.pack(side=tk.LEFT, padx=(0, 6), ipady=2)
        self.find_entry.bind("<KeyRelease>", lambda e: self.find_text_in_editor())
        self.find_entry.bind("<Return>", lambda e: self.find_text_in_editor(next_match=True))

        btn_find_next = tk.Button(self.find_frame, text="Berikutnya (Enter)", command=lambda: self.find_text_in_editor(next_match=True), bg=THEME["bg_input"], fg=THEME["text_main"], relief=tk.FLAT, font=("DejaVu Sans", 8), cursor="hand2")
        btn_find_next.pack(side=tk.LEFT, padx=(0, 6))

        btn_find_close = tk.Button(self.find_frame, text="✕", command=self.toggle_find_bar, bg=THEME["bg_input"], fg=THEME["text_muted"], relief=tk.FLAT, cursor="hand2")
        btn_find_close.pack(side=tk.LEFT)

        self.find_status_lbl = tk.Label(self.find_frame, text="", fg=THEME["accent_yellow"], bg=THEME["bg_surface"], font=("DejaVu Sans", 8))
        self.find_status_lbl.pack(side=tk.LEFT, padx=(10, 0))

        # 4. Text Editor Area dengan Line Numbers
        editor_container = tk.Frame(self, bg=THEME["bg_dark"], padx=14, pady=10)
        editor_container.pack(fill=tk.BOTH, expand=True)

        # Scrollbar horizontal dipasang DULU sebelum editor_box agar dapat ruang di bawah
        scroll_x = ttk.Scrollbar(editor_container, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        editor_box = tk.Frame(editor_container, bg=THEME["bg_dark"], highlightthickness=1, highlightbackground=THEME["border"])
        editor_box.pack(fill=tk.BOTH, expand=True)

        # Scrollbar vertikal
        scroll_y = ttk.Scrollbar(editor_box, orient=tk.VERTICAL, command=self._on_scroll_y)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas Nomor Baris
        self.line_canvas = tk.Canvas(
            editor_box,
            width=46,
            bg="#13131d",
            highlightthickness=0,
            borderwidth=0
        )
        self.line_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Text Widget
        self.text_editor = tk.Text(
            editor_box,
            bg=THEME["bg_dark"],
            fg=THEME["text_main"],
            insertbackground=THEME["accent_cyan"],
            selectbackground=THEME["selection"],
            selectforeground=THEME["text_main"],
            font=("DejaVu Sans Mono", 11),
            undo=True,
            wrap=tk.NONE,
            relief=tk.FLAT,
            padx=12,
            pady=8
        )
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbars ke text editor
        scroll_x.configure(command=self.text_editor.xview)
        self.text_editor.configure(yscrollcommand=self._on_text_scroll_y, xscrollcommand=scroll_x.set)

        # Event binding text editor
        self.text_editor.bind("<<Modified>>", self._on_text_modified)
        self.text_editor.bind("<KeyRelease>", self._on_key_release)
        self.text_editor.bind("<ButtonRelease-1>", lambda e: self.update_status_bar())
        self.text_editor.bind("<MouseWheel>", self._on_mousewheel)
        self.text_editor.bind("<Button-4>", self._on_mousewheel)
        self.text_editor.bind("<Button-5>", self._on_mousewheel)

        # Syntax tags styling
        self.text_editor.tag_configure("comment", foreground=THEME["highlight_comment"], font=("DejaVu Sans Mono", 11, "italic"))
        self.text_editor.tag_configure("give_cmd", foreground=THEME["highlight_give"], font=("DejaVu Sans Mono", 11, "bold"))
        self.text_editor.tag_configure("reset_cmd", foreground=THEME["highlight_reset"], font=("DejaVu Sans Mono", 11, "bold"))
        self.text_editor.tag_configure("search_match", background="#b58900", foreground="#ffffff")

        # Context menu klik kanan
        self.context_menu = tk.Menu(self, tearoff=0, bg=THEME["bg_card"], fg=THEME["text_main"], activebackground=THEME["selection"], activeforeground=THEME["accent_cyan"])
        self.context_menu.add_command(label="Potong (Cut)", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Salin (Copy)", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Tempel (Paste)", command=lambda: self.text_editor.event_generate("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Pilih Semua (Ctrl+A)", command=lambda: self.text_editor.tag_add(tk.SEL, "1.0", tk.END))
        self.text_editor.bind("<Button-3>", self.show_context_menu)

        # 5. Status Bar & Tips
        status_bar = tk.Frame(self, bg=THEME["bg_card"], padx=14, pady=6, highlightthickness=1, highlightbackground=THEME["border"])
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_detail_lbl = tk.Label(
            status_bar,
            text="Baris: 1 | Kolom: 1 | Total Argumen: 0",
            font=("DejaVu Sans", 9),
            fg=THEME["text_muted"],
            bg=THEME["bg_card"]
        )
        self.status_detail_lbl.pack(side=tk.LEFT)

        tips_lbl = tk.Label(
            status_bar,
            text="💡 Tips: Gunakan '#' di awal baris untuk catatan. Setiap token --give dieksekusi oleh server.",
            font=("DejaVu Sans", 8),
            fg=THEME["text_dim"],
            bg=THEME["bg_card"]
        )
        tips_lbl.pack(side=tk.RIGHT)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _on_scroll_y(self, *args):
        self.text_editor.yview(*args)
        self.redraw_line_numbers()

    def _on_text_scroll_y(self, *args):
        self.redraw_line_numbers()

    def _on_mousewheel(self, event):
        self.after(10, self.redraw_line_numbers)

    def redraw_line_numbers(self):
        self.line_canvas.delete("all")
        i = self.text_editor.index("@0,0")
        while True:
            dline = self.text_editor.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.line_canvas.create_text(
                40, y + 2,
                anchor=tk.NE,
                text=line_num,
                fill=THEME["text_dim"],
                font=("DejaVu Sans Mono", 9)
            )
            i = self.text_editor.index(f"{i}+1line")

    def _on_key_release(self, event=None):
        self.redraw_line_numbers()
        self.highlight_syntax()
        self.update_status_bar()

    def _on_text_modified(self, event=None):
        if self.text_editor.edit_modified():
            if not self.suppress_modified_event:
                self.set_modified(True)
            self.text_editor.edit_modified(False)

    def set_modified(self, modified: bool):
        self.is_modified = modified
        if modified:
            self.save_status_badge.config(text="● Belum Disimpan", fg=THEME["accent_yellow"])
            self.btn_save.config(bg="#f57c00")
        else:
            self.save_status_badge.config(text="● Tersimpan", fg=THEME["accent_green"])
            self.btn_save.config(bg="#1e88e5")

    def highlight_syntax(self):
        """Menyorot sintaks komentar (#), --give, dan --reset-account"""
        for tag in ["comment", "give_cmd", "reset_cmd"]:
            self.text_editor.tag_remove(tag, "1.0", tk.END)

        content = self.text_editor.get("1.0", tk.END)
        lines = content.split("\n")

        for line_idx, line in enumerate(lines, start=1):
            s_line = line.strip()
            if not s_line:
                continue

            # Komentar (# ...)
            if s_line.startswith("#"):
                start = f"{line_idx}.0"
                end = f"{line_idx}.end"
                self.text_editor.tag_add("comment", start, end)
                continue

            # Reset account
            if "--reset-account" in line:
                start_col = line.find("--reset-account")
                end_col = start_col + len("--reset-account")
                self.text_editor.tag_add("reset_cmd", f"{line_idx}.{start_col}", f"{line_idx}.{end_col}")

            # --give
            idx = 0
            while True:
                idx = line.find("--give", idx)
                if idx == -1:
                    break
                self.text_editor.tag_add("give_cmd", f"{line_idx}.{idx}", f"{line_idx}.{idx + 6}")
                idx += 6

    def toggle_find_bar(self):
        if self.find_frame.winfo_ismapped():
            self.find_frame.pack_forget()
            self.text_editor.tag_remove("search_match", "1.0", tk.END)
            self.text_editor.focus_set()
        else:
            self.find_frame.pack(fill=tk.X, side=tk.TOP, after=self.find_frame.master.winfo_children()[1])
            self.find_entry.focus_set()
            self.find_entry.select_range(0, tk.END)

    def find_text_in_editor(self, next_match=False):
        self.text_editor.tag_remove("search_match", "1.0", tk.END)
        query = self.find_var.get()
        if not query:
            self.find_status_lbl.config(text="")
            return

        start = "1.0"
        if next_match:
            try:
                start = self.text_editor.index(tk.INSERT + "+1c")
            except Exception:
                start = "1.0"

        matches = 0
        first_pos = None

        cur = "1.0"
        while True:
            cur = self.text_editor.search(query, cur, stopindex=tk.END, nocase=True)
            if not cur:
                break
            end = f"{cur}+{len(query)}c"
            self.text_editor.tag_add("search_match", cur, end)
            if not first_pos:
                first_pos = cur
            matches += 1
            cur = end

        # Temukan match berikutnya setelah start
        pos = self.text_editor.search(query, start, stopindex=tk.END, nocase=True)
        if not pos and first_pos:
            pos = first_pos

        if pos:
            self.text_editor.mark_set(tk.INSERT, pos)
            self.text_editor.see(pos)
            self.find_status_lbl.config(text=f"{matches} kecocokan ditemukan")
        else:
            self.find_status_lbl.config(text="Tidak ditemukan")

    def update_status_bar(self):
        try:
            cur_index = self.text_editor.index(tk.INSERT)
            line, col = cur_index.split(".")
        except Exception:
            line, col = 1, 0

        content = self.text_editor.get("1.0", tk.END)
        lines = [l.strip() for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]
        arg_count = sum(len(l.split()) for l in lines)
        total_lines = int(self.text_editor.index('end-1c').split('.')[0])

        self.status_detail_lbl.config(
            text=f"Baris: {line}/{total_lines} | Kolom: {int(col)+1} | Argumen Aktif: {arg_count}"
        )

    def setup_shortcuts(self):
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-S>", lambda e: self.save_file())
        self.bind("<Control-f>", lambda e: self.toggle_find_bar())
        self.bind("<Control-F>", lambda e: self.toggle_find_bar())
        self.bind("<Control-r>", lambda e: self.reset_content())
        self.bind("<Control-R>", lambda e: self.reset_content())
        self.bind("<Control-o>", lambda e: self.reload_file())
        self.bind("<Control-O>", lambda e: self.reload_file())
        self.bind("<F5>", lambda e: self.run_server_in_terminal())
        self.bind("<Escape>", lambda e: self.on_escape_key())

    def on_escape_key(self):
        if self.find_frame.winfo_ismapped():
            self.toggle_find_bar()

    def load_file(self):
        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.write("# Argumen Server FF7EC Offline\n--give gil=80000000\n")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membuat file {self.file_path}: {e}")
                return

        try:
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            self.suppress_modified_event = True
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", content)
            self.suppress_modified_event = False

            self.set_modified(False)
            self.highlight_syntax()
            self.redraw_line_numbers()
            self.update_status_bar()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca {self.file_path}: {e}")

    def save_file(self):
        content = self.text_editor.get("1.0", tk.END)
        content = content.rstrip("\r\n") + "\n"

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.set_modified(False)
            #messagebox.showinfo("Tersimpan", f"Perubahan berhasil disimpan ke:\n{self.file_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {e}")
            return False

    def reload_file(self):
        if self.is_modified:
            if not messagebox.askyesno("Muat Ulang", "Ada perubahan yang belum disimpan. Yakin ingin memuat ulang dari file?"):
                return
        self.load_file()

    def reset_content(self):
        """Tombol reset untuk mengosongkan editor"""
        if messagebox.askyesno("Konfirmasi Kosongkan", "Apakah Anda yakin ingin MENGOSONGKAN seluruh isi server_args.txt di editor?\n\n(Tindakan ini akan menghapus semua argumen dari editor)"):
            self.suppress_modified_event = True
            self.text_editor.delete("1.0", tk.END)
            self.suppress_modified_event = False
            self.set_modified(True)
            self.redraw_line_numbers()
            self.highlight_syntax()
            self.update_status_bar()

    def open_item_helper(self):
        """Membuka pop-up dialog bantuan pemilih item"""
        ItemHelperDialog(self, self.db, self.insert_entry)

    def insert_entry(self, entry_text: str, append: bool = True):
        """Menambahkan entry teks ke editor (append di akhir atau insert di kursor)"""
        current_content = self.text_editor.get("1.0", tk.END)

        if append:
            if current_content.strip():
                if not current_content.endswith("\n\n"):
                    if not current_content.endswith("\n"):
                        self.text_editor.insert(tk.END, "\n\n")
                    else:
                        self.text_editor.insert(tk.END, "\n")
            self.text_editor.insert(tk.END, entry_text + "\n")
            self.text_editor.see(tk.END)
        else:
            self.text_editor.insert(tk.INSERT, entry_text + "\n")

        self.set_modified(True)
        self.highlight_syntax()
        self.redraw_line_numbers()
        self.update_status_bar()

    def apply_preset_starter(self):
        if messagebox.askyesno("Terapkan Preset", "Terapkan preset Starter Pack Kaya (Gil, Crystals, Stamina, Medali)?"):
            starter = (
                "# === MATA UANG & STAMINA ===\n"
                "--give gil=500000000\n"
                "--give crystals=50000\n"
                "--give red_crystals=10000\n"
                "--give stamina=999\n"
                "--give chocobo_medals=50000\n"
                "--give weapon_medals=50000\n"
                "--give crisis_medals=50000\n"
            )
            self.insert_entry(starter, append=True)

    def apply_preset_all_unlocks(self):
        if messagebox.askyesno("Terapkan Preset", "Terapkan preset pembuka semua Kostum, Wallpaper, dan Memoria?"):
            unlocks = (
                "# === BUKA SEMUA KOSTUM, WALLPAPER & MEMORIA ===\n"
                "--give costume=all\n"
                "--give wallpaper=all\n"
                "--give memoria=all\n"
            )
            self.insert_entry(unlocks, append=True)

    def apply_preset_reset_account(self):
        if messagebox.askyesno("Terapkan Preset", "Terapkan flag --reset-account untuk mereset akun offline dari awal?"):
            self.insert_entry("# Reset akun server ke kondisi awal baru\n--reset-account\n", append=True)

    def check_save_before_run(self):
        if self.is_modified:
            ans = messagebox.askyesnocancel("Simpan Perubahan", "Ada perubahan pada argumen yang belum disimpan.\n\nSimpan sekarang sebelum menjalankan server?")
            if ans is None:  # Batal
                return False
            elif ans is True:  # Simpan
                if not self.save_file():
                    return False
        return True

    def run_server_in_terminal(self):
        """Jalankan start_offline.sh langsung di terminal eksternal (Kitty / Alacritty)"""
        if not self.check_save_before_run():
            return

        cmd_str = f"cd '{SCRIPT_DIR}' && bash '{START_SCRIPT_PATH}'"
        terminal_candidates = [
            ("kitty", ["kitty", "--title", "FF7EC Offline Server", "bash", "-c", cmd_str]),
            ("alacritty", ["alacritty", "--title", "FF7EC Offline Server", "-e", "bash", "-c", cmd_str]),
            ("x-terminal-emulator", ["x-terminal-emulator", "-e", "bash", "-c", cmd_str]),
        ]

        for term_name, term_cmd in terminal_candidates:
            if subprocess.run(["which", term_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                try:
                    subprocess.Popen(term_cmd, cwd=SCRIPT_DIR)
                    #messagebox.showinfo("Server Berjalan", f"Server offline berhasil dijalankan di terminal {term_name}.")
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal membuka terminal {term_name}: {e}")
                    return

        messagebox.showwarning("Terminal Tidak Ditemukan", "Tidak menemukan Kitty atau Alacritty di sistem.")


def main():
    app = ArgsEditorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
