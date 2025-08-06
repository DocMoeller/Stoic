# Auto Website App Launcher - Frameless Window
# Dette program åbner automatisk en hjemmeside som en app uden browser-chrome
# Kan også fjerne Windows-rammen helt

import subprocess
import webbrowser
import sys
import os
import websocket
import json


class AutoWebAppLauncher:
    def __init__(self, url="https://netflix.com", frameless=False, kiosk_mode=False):
        """
        url: URL til at åbne
        frameless: Forsøg at fjerne browser-rammen (kun Chrome app mode)
        kiosk_mode: Fuld kiosk mode (fjerner alt)
        """
        self.url = url
        self.frameless = frameless
        self.kiosk_mode = kiosk_mode

        # Standard zoom-niveau (100%)
        self.zoom_level = 130

        # Sørg for at URL har protocol
        if not self.url.startswith(('http://', 'https://')):
            self.url = 'https://' + self.url

    def set_zoom(self, zoom_level):
        """Indstil zoom-niveau"""
        self.zoom_level = zoom_level

    def get_zoom_argument(self):
        """Returner zoom-argument til browseren"""
        return f"--force-device-scale-factor={self.zoom_level / 100}"

    def launch_chrome_app(self):
        """Start Chrome i app mode med forskellige ramme-indstillinger"""
        print(f"🚀 Forsøger Chrome for {self.url}...")

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome"
        ]

        # Base Chrome argumenter for app mode
        chrome_args = [
            f"--app={self.url}",
            "--no-first-run",
            "--disable-default-apps",
            "--disable-features=TranslateUI",
            "--disable-ipc-flooding-protection"
        ]

        # Tilføj frameless argumenter
        if self.frameless or self.kiosk_mode:
            chrome_args.extend([
                "--disable-frame-type-hinting",
                "--disable-background-mode",
                "--disable-background-networking"
            ])

        # Fuld kiosk mode
        if self.kiosk_mode:
            chrome_args.extend([
                "--kiosk",
                "--start-fullscreen",
                "--disable-restore-session-state",
                "--disable-application-cache",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-java",
                "--disable-javascript-harmony-shipping",
                "--disable-translate",
                "--no-default-browser-check",
                "--disable-infobars",
                "--disable-notifications",
                "--disable-save-password-bubble"
            ])
        elif self.frameless:
            # Forsøg mere minimalistisk tilgang
            chrome_args.extend([
                "--window-position=0,0",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ])

        # Tilføj zoom argument
        chrome_args.append(self.get_zoom_argument())

        # Forsøg at starte Chrome
        for chrome_path in chrome_paths:
            try:
                subprocess.Popen([chrome_path] + chrome_args)
                print(f"✅ Chrome app startet!")
                if self.kiosk_mode:
                    print("📺 Kiosk mode aktiveret - tryk Alt+F4 for at lukke")
                elif self.frameless:
                    print(
                        "🪟 Frameless mode forsøgt - kan variere afhængigt af Chrome version")
                return True
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️ Fejl med {chrome_path}: {e}")
                continue

        return False

    def launch_edge_app(self):
        """Start Microsoft Edge i app mode"""
        print(f"🚀 Forsøger Edge for {self.url}...")

        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            "msedge"
        ]

        # Edge argumenter (ligner Chrome)
        edge_args = [
            f"--app={self.url}",
            "--no-first-run",
            "--disable-default-apps"
        ]

        if self.kiosk_mode:
            edge_args.extend([
                "--kiosk",
                "--start-fullscreen",
                "--disable-extensions"
            ])
        elif self.frameless:
            edge_args.extend([
                "--window-position=0,0"
            ])

        # Tilføj zoom argument
        edge_args.append(self.get_zoom_argument())

        for edge_path in edge_paths:
            try:
                subprocess.Popen([edge_path] + edge_args)
                print(f"✅ Edge app startet!")
                if self.kiosk_mode:
                    print("📺 Edge kiosk mode aktiveret")
                return True
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️ Fejl med {edge_path}: {e}")
                continue

        return False

    def launch_firefox_app(self):
        """Start Firefox i kiosk mode"""
        print(f"🚀 Forsøger Firefox for {self.url}...")

        firefox_paths = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            r"C:\Users\{}\AppData\Local\Mozilla Firefox\firefox.exe".format(
                os.getenv('USERNAME', '')),
            "firefox"
        ]

        # Firefox argumenter
        if self.kiosk_mode:
            firefox_args = [
                "--kiosk",
                self.url
            ]
        else:
            # Firefox har ikke --app mode som Chrome/Edge
            firefox_args = [
                "--new-window",
                self.url
            ]

        # Firefox understøtter ikke direkte zoom-argumenter som Chrome/Edge

        for firefox_path in firefox_paths:
            try:
                subprocess.Popen([firefox_path] + firefox_args)
                print(f"✅ Firefox startet!")
                if self.kiosk_mode:
                    print("📺 Firefox kiosk mode aktiveret")
                else:
                    print("🪟 Firefox i nyt vindue (ingen app mode)")
                return True
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️ Fejl med {firefox_path}: {e}")
                continue

        return False

    def launch_fallback(self):
        """Fallback til standard browser"""
        print(
            "⚠️ Ingen af de specificerede browsere blev fundet. Åbner i standard browser...")
        webbrowser.open(self.url)

    def inject_javascript(self, script):
        """Injicerer JavaScript i browseren"""
        print("⚙️ Injicerer JavaScript...")

        # Chrome debugging port
        debug_port = 9222

        # Start Chrome med debugging aktiveret
        chrome_paths = [
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "chrome"
        ]

        for chrome_path in chrome_paths:
            try:
                subprocess.Popen([
                    chrome_path,
                    f"--remote-debugging-port={debug_port}",
                    f"--app={self.url}"
                ])
                break
            except FileNotFoundError:
                continue

        # Brug websocket til at kommunikere med browseren
        try:
            ws = websocket.create_connection(
                f"ws://localhost:{debug_port}/devtools/browser")

            # Forbedret script med ventelogik
            enhanced_script = """
            (function waitForVideo() {
                var checkInterval = setInterval(function() {
                    var video = document.querySelector('video');
                    if (video) {
                        clearInterval(checkInterval);
                        video.style.transform = 'scale(1.5)';
                        video.style.transformOrigin = 'center';
                        console.log('✅ Video fundet og zoomet ind.');
                    } else {
                        console.log('⏳ Venter på videoelement...');
                    }
                }, 1000);
            })();
            """

            ws.send(json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": enhanced_script
                }
            }))
            response = ws.recv()
            print(f"✅ JavaScript injiceret: {response}")
            ws.close()
        except Exception as e:
            print(f"⚠️ Fejl ved injektion af JavaScript: {e}")

    def launch(self):
        """Start app launcher - prøver flere browsere"""
        print("🔍 Søger efter tilgængelige browsere...")

        # Forsøg Chrome først
        success = self.launch_chrome_app()
        if success:
            return

        # Så Edge
        success = self.launch_edge_app()
        if success:
            return

        # Fallback til standard browser
        self.launch_fallback()


def main():
    """Main funktion - kan konfigureres her"""

    # Konfiguration
    URL = "https://netflix.com"  # Ændr denne URL til din foretrukne side
    FRAMELESS = True            # Forsøg at fjerne browser-rammen
    KIOSK_MODE = True           # Fuld kiosk mode (fjerner alt)
    PREFERRED_BROWSER = "auto"  # "chrome", "edge", eller "auto"

    print("🌐 Auto Website App Launcher")
    print("=" * 40)
    print(f"URL: {URL}")
    print(f"Frameless: {FRAMELESS}")
    print(f"Kiosk Mode: {KIOSK_MODE}")
    print(f"Foretrukken Browser: {PREFERRED_BROWSER}")
    print()

    # Start launcher
    launcher = AutoWebAppLauncher(
        url=URL,
        frameless=FRAMELESS,
        kiosk_mode=KIOSK_MODE
    )

    # Indstil zoom-niveau
    launcher.set_zoom(150)  # Zoom til 150%

    # Start baseret på browser-præference
    if PREFERRED_BROWSER == "chrome":
        success = launcher.launch_chrome_app()
        if not success:
            launcher.launch_fallback()
    elif PREFERRED_BROWSER == "edge":
        success = launcher.launch_edge_app()
        if not success:
            launcher.launch_fallback()
    else:
        # Auto mode - prøv alle browsere
        launcher.launch()

    # Eksempel på JavaScript til at zoome ind på en video
    zoom_script = """
    var video = document.querySelector('video');
    if (video) {
        video.style.transform = 'scale(1.5)';
        video.style.transformOrigin = 'center';
    } else {
        console.log('Ingen video fundet på siden.');
    }
    """

    # Injicer JavaScript
    launcher.inject_javascript(zoom_script)


if __name__ == "__main__":
    main()
