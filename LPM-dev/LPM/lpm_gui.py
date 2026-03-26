import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import yaml
import os
import tempfile
import subprocess
import lpm_builder

CATEGORIES = {
    "AudioVideo": "Audio & Video",
    "Development": "Development",
    "Education": "Education",
    "Game": "Games",
    "Graphics": "Graphics",
    "Network": "Network",
    "Office": "Office",
    "Science": "Science",
    "Settings": "Settings",
    "System": "System",
    "Utility": "Utilities"
}

DESKTOP_ICON_CHOICES = [
    "Let the user decide",
    "Create a desktop icon",
    "Do not create a desktop icon"
]

APP_TYPES = ["Graphical", "Console"]
COMPRESSION_TYPES = ["xz", "gz"]

LABELS = {
    "AppName": "Application name",
    "AppDirectory": "Application directory",
    "Launcher": "Main executable",
    "Icon": "Icon",
    "Category": "Category",
    "ShortDescription": "Short description",
    "Description": "Detailed description",
    "Version": "Version",
    "Author": "Author",
    "DesktopIcon": "Desktop icon",
    "AppType": "Application type",
    "Command": "Shell command",
    "InstFileName": "Installer file name",
    "CompressionMode": "Compression mode"
}

TOOLTIPS = {
    "AppName": "Displayed application name",
    "AppDirectory": "Directory containing all application files",
    "Launcher": "Main executable (must be inside the directory)",
    "Icon": "Application icon",
    "Category": "Category in the system menu",
    "ShortDescription": "Short description",
    "Description": "Detailed description",
    "Version": "Application version",
    "Author": "Author",
    "DesktopIcon": "Create a desktop icon",
    "AppType": "Graphical or console",
    "Command": "Command used to launch the application",
    "InstFileName": "Generated .lpk file name",
    "CompressionMode": "Compression type"
}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        if self.tip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None




def apply_theme(style):
    style.theme_use("default")

    # Palette claire
    bg = "#cffffb"
    fg = "#2b2d42"
    accent = "#4f8cff"
    accent_hover = "#3a6fd8"
    entry_bg = "#ffffff"
    border = "#dcdde1"

    # Global
    style.configure(
        ".",
        background=bg,
        foreground=fg,
        font=("Noto Sans", 10)
    )

    # Labels
    style.configure(
        "TLabel",
        background=bg,
        foreground=fg,
        padding=4
    )

    # Boutons "arrondis"
    style.configure(
        "Rounded.TButton",
        background=accent,
        foreground="white",
        borderwidth=0,
        padding=(14, 8),
        relief="flat"
    )

    style.map(
        "Rounded.TButton",
        background=[
            ("active", accent_hover),
            ("pressed", accent_hover)
        ],
        foreground=[
            ("disabled", "#aaaaaa")
        ]
    )

    # Hack visuel pour effet arrondi (padding + focus off)
    style.layout("Rounded.TButton", [
        ("Button.border", {
            "sticky": "nswe",
            "children": [
                ("Button.focus", {
                    "sticky": "nswe",
                    "children": [
                        ("Button.padding", {
                            "sticky": "nswe",
                            "children": [
                                ("Button.label", {"sticky": "nswe"})
                            ]
                        })
                    ]
                })
            ]
        })
    ])

    # Entrées
    style.configure(
        "TEntry",
        fieldbackground=entry_bg,
        background=entry_bg,
        foreground=fg,
        bordercolor=border,
        lightcolor=border,
        darkcolor=border,
        padding=6,
        relief="flat"
    )

    style.map(
        "TEntry",
        bordercolor=[("focus", accent)],
        fieldbackground=[("focus", "#eef3ff")]
    )



class LPMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Package Maker - Graphical wizard")
        self.root.resizable(False, False)

        style = ttk.Style()
        apply_theme(style)

        self.entries = {}

        main = ttk.Frame(root, padding=10)
        main.grid(sticky="nsew")

        row = 0

        row = self.add_entry(main, row, "AppName", required=True)
        row = self.add_entry(main, row, "AppDirectory", browse=True, is_dir=True, required=True)
        row = self.add_entry(main, row, "Launcher", browse=True, required=True)
        row = self.add_entry(main, row, "Icon", browse=True)

        ttk.Separator(main).grid(row=row, column=0, columnspan=4, sticky="ew", pady=10)
        row += 1

        row = self.add_combobox(main, row, "Category", list(CATEGORIES.values()))
        row = self.add_entry(main, row, "ShortDescription")
        row = self.add_entry(main, row, "Description")
        row = self.add_entry(main, row, "Version", default="1.0")
        row = self.add_entry(main, row, "Author")

        ttk.Separator(main).grid(row=row, column=0, columnspan=4, sticky="ew", pady=10)
        row += 1

        row = self.add_desktop_icon_choice(main, row)
        row = self.add_combobox(main, row, "AppType", APP_TYPES)
        row = self.add_entry(main, row, "Command")

        ttk.Separator(main).grid(row=row, column=0, columnspan=4, sticky="ew", pady=10)
        row += 1

        row = self.add_entry(main, row, "InstFileName")
        row = self.add_combobox(main, row, "CompressionMode", COMPRESSION_TYPES)

        ttk.Button(main, text="Generate file", command=self.generate_yaml, style = "Rounded.TButton").grid(row=row, column=0, pady=10)
        ttk.Button(main, text="Generate installer", command=self.generate_installer, style = "Rounded.TButton").grid(row=row, column=1, pady=10)
        ttk.Button(main, text="Load file", command=self.load_yaml, style = "Rounded.TButton").grid(row=row, column=2, pady=10)

    def validate_ascii(self, text):
        try:
            text.encode("ascii")
            return True
        except:
            return False

    def add_entry(self, parent, row, name, browse=False, is_dir=False, default=None, required=False):
        label = ttk.Label(parent, text=LABELS[name] + (" *" if required else ""))
        label.grid(row=row, column=0, sticky="w", padx=(0,10))
        ToolTip(label, TOOLTIPS[name])
        entry = ttk.Entry(parent, width=40)
        entry.grid(row=row, column=1, sticky="ew", padx=(0,10))

        if default:
            entry.insert(0, default)

        if name == "AppName":
            entry.bind("<KeyRelease>", self.update_installer_name)

        if browse:
            entry.config(state="readonly")
            def browse_cmd():
                path = filedialog.askdirectory() if is_dir else filedialog.askopenfilename()
                if path:
                    entry.config(state="normal")
                    entry.delete(0, tk.END)
                    entry.insert(0, path)
                    entry.config(state="readonly")
                self.update_installer_name()

            ttk.Button(parent, text="Browse", command=browse_cmd, style = "Rounded.TButton").grid(row=row, column=2)

        self.entries[name] = entry
        return row + 1

    def update_installer_name(self, event=None):
        name = self.entries["AppName"].get()
        directory = lpm_builder.getFileDirectory(self.entries["AppDirectory"].get())
        if name:
            self.entries["InstFileName"].delete(0, tk.END)
            self.entries["InstFileName"].insert(0, directory + '/' + name + "_installer")

    def add_combobox(self, parent, row, name, values, default=None):
        label = ttk.Label(parent, text=LABELS[name])
        label.grid(row=row, column=0, sticky="w", padx=(0,10))
        ToolTip(label, TOOLTIPS[name])
        combo = ttk.Combobox(parent, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", padx=(0,10))

        if default:
            combo.set(default)

        self.entries[name] = combo
        return row + 1

    def add_desktop_icon_choice(self, parent, row):
        label = ttk.Label(parent, text=LABELS["DesktopIcon"])
        label.grid(row=row, column=0, sticky="w", padx=(0,10))
        ToolTip(label, TOOLTIPS["DesktopIcon"])
        combo = ttk.Combobox(parent, values=DESKTOP_ICON_CHOICES, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", padx=(0,10))

        combo.set(DESKTOP_ICON_CHOICES[0])
        self.entries["DesktopIcon"] = combo
        return row + 1

    def build_data(self):
        data = {}

        app_dir = self.entries["AppDirectory"].get()
        launcher = self.entries["Launcher"].get()

        for key in ["AppName", "AppDirectory", "Launcher"]:
            val = self.entries[key].get()
            if not val:
                messagebox.showerror("Error", f"Missing field: {LABELS[key]}")
                return None
            if not self.validate_ascii(val):
                messagebox.showerror("Error", f"Non-ASCII characters in {LABELS[key]}")
                return None

        try:
            rel_path = os.path.relpath(launcher, app_dir)
            if rel_path.startswith(".."):
                raise ValueError
        except:
            messagebox.showerror("Error", "Launcher must be inside AppDirectory")
            return None

        data["AppName"] = self.entries["AppName"].get()
        data["AppDirectory"] = app_dir
        data["Launcher"] = rel_path

        for key, val in self.entries.items():
            if key in data:
                continue

            if key == "DesktopIcon":
                if val.get() == DESKTOP_ICON_CHOICES[1]:
                    data[key] = True
                elif val.get() == DESKTOP_ICON_CHOICES[2]:
                    data[key] = False
                continue

            if key == "AppType":
                data["Terminal"] = (val.get() == "Console")
                continue

            if key == "Category":
                for k, v in CATEGORIES.items():
                    if v == val.get():
                        data[key] = k
                continue

            v = val.get()
            if v:
                if not self.validate_ascii(v):
                    messagebox.showerror("Error", f"Non-ASCII characters in {LABELS[key]}")
                    return None
                data[key] = v

        return data

    def generate_yaml(self):
        data = self.build_data()
        if data is None:
            return

        file = filedialog.asksaveasfilename(defaultextension=".yaml")
        if file:
            with open(file, "w") as f:
                yaml.dump(data, f, sort_keys=False)
            messagebox.showinfo("Success", f"File generated:\n{file}")

    def generate_installer(self):
        data = self.build_data()
        if data is None:
            return

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode="w") as tmp:
                yaml.dump(data, tmp)
                tmp_path = tmp.name

            lpm_builder.build_installer(tmp_path)
            os.remove(tmp_path)
            messagebox.showinfo("Success", "Installer generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_yaml(self):
        file = filedialog.askopenfilename(filetypes=[("YAML", "*.yaml *.yml")])
        if not file:
            return

        with open(file) as f:
            data = yaml.safe_load(f)

        for key, val in data.items():
            if key not in self.entries:
                continue

            widget = self.entries[key]

            if key == "DesktopIcon":
                widget.set(DESKTOP_ICON_CHOICES[1] if val else DESKTOP_ICON_CHOICES[2])
            elif key == "Terminal":
                self.entries["AppType"].set("Console" if val else "Graphical")
            elif key == "Category":
                widget.set(CATEGORIES.get(val, ""))
            else:
                if key == "AppDirectory" or key == "Icon":
                    val = lpm_builder.solve_relative_path(lpm_builder.getFileDirectory(file), val)
                elif key == "Launcher":
                    val = lpm_builder.solve_relative_path(lpm_builder.getFileDirectory(file), data["AppDirectory"]) + '/' + val

                widget.config(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, str(val))
                if widget.cget("state") == "readonly":
                    widget.config(state="readonly")

        if self.entries["InstFileName"].get() == "":
            self.update_installer_name()


def launch_app():
    root = tk.Tk()
    app = LPMGui(root)
    root.mainloop()
