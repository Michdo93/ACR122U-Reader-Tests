import nfc
import sys
import nfc.clf
from nfc.tag import TagCommandError

# Der Standard-Key A (vom Hersteller voreingestellt oder bekannt)
MIFARE_KEY = b'\xff\xff\xff\xff\xff\xff'

# Daten, die geschrieben werden sollen (16 Bytes)
# Hier: Der Text "Hallo Welt!" mit Leerzeichen und Nullen aufgefüllt
DATA_TO_WRITE = b'Hallo Welt!     ' # Muss genau 16 Bytes lang sein!

def write_mifare(tag):
    """Schreibt Daten in Block 1 von Sektor 1 einer MIFARE Classic Karte."""
    try:
        if tag.type != 'Mifare Classic 1K':
             print("❌ Tag ist keine MIFARE Classic 1K Karte.")
             return

        # Authentifizierung für Sektor 1
        tag.authenticate(1, nfc.tag.block(4), MIFARE_KEY)

        print(f"Schreibe Daten: {DATA_TO_WRITE.decode('utf-8')}")
        
        # Schreibe die 16 Bytes in Block 1 (Datenblock im Sektor 1)
        tag.write(nfc.tag.block(1), DATA_TO_WRITE)

        print("✅ Schreiben erfolgreich.")

    except TagCommandError:
        print("❌ Authentifizierung fehlgeschlagen. Falscher Schlüssel oder Schreibschutz?")
    except ValueError as ve:
        print(f"❌ Fehler: {ve} (Stellen Sie sicher, dass die Daten genau 16 Bytes lang sind!)")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben: {e}", file=sys.stderr)

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        if not clf:
            print("❌ NFC-Reader (ACR122U) nicht gefunden.")
            return
        
        print("NFC Reader gefunden. Halten Sie eine MIFARE Classic Karte an den Reader...")
        clf.connect(rdwr={'on-connect': write_mifare, 'targets': ('mfc',)})

if __name__ == '__main__':
    main()
