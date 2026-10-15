# Mobile-friendly Sentinel SMS & URL Threat Analyzer

The responsive frontend adapts to desktop, tablet, and mobile screens. On small screens, navigation becomes a compact row, metric cards stack vertically, and the SMS and URL scanners appear one after another.

## Run on your computer
1. Extract the ZIP.
2. Double-click `RUN_PROJECT.bat`, or run `py app.py` from PowerShell in this folder.
3. Open `http://127.0.0.1:5000/` on the same computer.

## Open on a phone on the same Wi-Fi
`127.0.0.1` on your phone refers to the phone itself, not your computer. To test on a phone, start Flask on your computer using `app.run(host="0.0.0.0", port=5000, ...)`, then open `http://YOUR-COMPUTER-LAN-IP:5000/` on the phone while both devices are on the same Wi-Fi. You may need to allow Python through Windows Firewall. Only do this on a trusted private network; do not expose the development server to the public internet.
