# Simple Website Viewer - Virker med standard Python
import tkinter as tk
from tkinter import ttk
import webbrowser
import subprocess
import sys
import os


class WebsiteViewerSimple:
    def __init__(self):
        self.root = tk.Tk()
        self.url = "https://netflix.com"  # Skift til din ønskede hjemmeside
        self.setup_gui()

    def setup_gui(self):
        """Opsæt GUI"""
        self.root.title("Website Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')

        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🌐 Website Viewer",
            font=('Arial', 18, 'bold'),
            bg='#34495e',
            fg='white'
        )
        title_label.pack(pady=20)

        # URL kontrolpanel
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(control_frame, text="URL:", bg='#2c3e50',
                 fg='white', font=('Arial', 12)).pack(side=tk.LEFT)

        self.url_entry = tk.Entry(control_frame, font=('Arial', 11), width=50)
        self.url_entry.pack(side=tk.LEFT, padx=(
            10, 10), fill=tk.X, expand=True)
        self.url_entry.insert(0, self.url)

        # Knapper
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(fill=tk.X, padx=20, pady=5)

        buttons = [
            ("🚀 Åbn i Nyt Vindue", self.open_in_new_window),
            ("🌍 Åbn i Browser", self.open_in_browser),
            ("📱 Åbn som App", self.open_as_app),
            ("⚙️ Indstillinger", self.show_settings)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg='#3498db',
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Instruktioner
        instructions_frame = tk.Frame(self.root, bg='#2c3e50')
        instructions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        instructions_text = """
🎯 Sådan bruger du Website Viewer:

1. 🚀 Nyt Vindue: Åbner hjemmesiden i et rent popup-vindue
2. 🌍 Browser: Åbner hjemmesiden i din standard browser
3. 📱 Som App: Åbner hjemmesiden i app-mode (Chrome)
4. ⚙️ Indstillinger: Tilpas viewer-indstillinger

💡 Tips: 
- For bedste oplevelse, installer Chrome
- App-mode skjuler browser-elementer
- Popup-vinduer kan blokeres af browseren

🔧 For embedded browser (iframe-lignende):
   pip install pywebview
   
   Derefter genstart programmet for avancerede funktioner.
        """

        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Arial', 10),
            justify=tk.LEFT,
            anchor='nw'
        )
        instructions_label.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Klar til brug")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            bg='#34495e',
            fg='white',
            font=('Arial', 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_url(self):
        """Hent URL fra input feltet"""
        url = self.url_entry.get().strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def open_in_new_window(self):
        """Åbn i popup vindue"""
        url = self.get_url()
        self.status_var.set(f"Åbner {url} i nyt vindue...")

        # Opret en HTML fil der åbner popup automatisk
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Website Launcher</title>
</head>
<body>
    <h2>Åbner {url}...</h2>
    <p>Hvis vinduet ikke åbner automatisk, <a href="#" onclick="openWindow()">klik her</a></p>
    
    <script>
        function openWindow() {{
            const width = 1200;
            const height = 800;
            const left = (screen.width - width) / 2;
            const top = (screen.height - height) / 2;
            
            window.open(
                "{url}",
                "websiteViewer",
                `width=${{width}},height=${{height}},top=${{top}},left=${{left}},` +
                `resizable=yes,scrollbars=yes,toolbar=no,location=no,menubar=no,status=no`
            );
        }}
        
        // Åbn automatisk
        window.onload = function() {{
            openWindow();
        }};
    </script>
</body>
</html>
        """

        # Gem temp HTML fil
        temp_file = os.path.join(os.path.dirname(
            __file__), "temp_launcher.html")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Åbn HTML filen
        webbrowser.open(f'file:///{temp_file}')

    def open_in_browser(self):
        """Åbn i standard browser"""
        url = self.get_url()
        self.status_var.set(f"Åbner {url} i browser...")
        webbrowser.open(url)

    def open_as_app(self):
        """Åbn som app (Chrome app mode)"""
        url = self.get_url()
        self.status_var.set(f"Åbner {url} som app...")

        # Forsøg at åbne i Chrome app mode
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome"  # Hvis Chrome er i PATH
        ]

        for chrome_path in chrome_paths:
            try:
                subprocess.Popen([
                    chrome_path,
                    f"--app={url}",
                    "--no-first-run",
                    "--disable-default-apps"
                ])
                return
            except (FileNotFoundError, subprocess.SubprocessError):
                continue

        # Fallback til normal browser
        self.status_var.set("Chrome ikke fundet. Åbner i standard browser...")
        webbrowser.open(url)

    def show_settings(self):
        """Vis indstillinger"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Indstillinger")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#2c3e50')

        tk.Label(
            settings_window,
            text="⚙️ Indstillinger",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)

        # Vinduesstørrelse
        size_frame = tk.Frame(settings_window, bg='#2c3e50')
        size_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(size_frame, text="Vinduesstørrelse:",
                 bg='#2c3e50', fg='white').pack(anchor='w')

        size_options = [
            ("Klein (800x600)", "800x600"),
            ("Medium (1200x800)", "1200x800"),
            ("Stor (1600x1000)", "1600x1000"),
            ("Fuldskærm", "fullscreen")
        ]

        for text, value in size_options:
            tk.Radiobutton(
                size_frame,
                text=text,
                value=value,
                bg='#2c3e50',
                fg='white',
                selectcolor='#3498db'
            ).pack(anchor='w')

    def run(self):
        """Start programmet"""
        self.root.mainloop()


if __name__ == "__main__":
    print("🌐 Starting Website Viewer...")
    app = WebsiteViewerSimple()
    app.run()
