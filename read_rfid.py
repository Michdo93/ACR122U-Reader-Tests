import nfc
import sys
import nfc.clf
from nfc.tag import TagCommandError

# Der Standard-Key A (vom Hersteller voreingestellt oder bekannt)
MIFARE_KEY = b'\xff\xff\xff\xff\xff\xff'

def read_mifare(tag):
    """Liest Block 1 von Sektor 1 einer MIFARE Classic Karte."""
    try:
        if tag.type != 'Mifare Classic 1K':
             print("❌ Tag ist keine MIFARE Classic 1K Karte.")
             return

        # Authentifizierung für Sektor 1 (Block 4 bis 7)
        # Wir verwenden den Block 4 (Sektor-Trailer) für die Authentifizierung
        tag.authenticate(1, nfc.tag.block(4), MIFARE_KEY)

        # Lese Block 1 (Datenblock im Sektor 1)
        # Die Methode read() gibt die 16 Bytes (1 Block) zurück
        data = tag.read(nfc.tag.block(1))

        print("✅ Lesen erfolgreich.")
        print(f"Gelesene Daten (Block 1, Sektor 1): {data.hex()}")

    except TagCommandError:
        print("❌ Authentifizierung fehlgeschlagen. Falscher Schlüssel?")
    except Exception as e:
        print(f"❌ Fehler beim Lesen: {e}", file=sys.stderr)

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        if not clf:
            print("❌ NFC-Reader (ACR122U) nicht gefunden.")
            return
        
        print("NFC Reader gefunden. Halten Sie eine MIFARE Classic Karte an den Reader...")
        # 'mfc' steht für MIFARE Classic
        clf.connect(rdwr={'on-connect': read_mifare, 'targets': ('mfc',)})

if __name__ == '__main__':
    main()
