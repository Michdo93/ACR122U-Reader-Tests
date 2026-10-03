import nfc
import sys
from nfc.ndef import Record, Message

# Die URL, die auf den Tag geschrieben werden soll
URL_TO_WRITE = "https://www.google.com"

def write_tag(tag):
    """Schreibt eine NDEF-Nachricht (URL) auf den Tag."""
    try:
        # Erstelle einen URI-Record
        record = Record('urn', "nfcforum.org:def:uri", 'u', URL_TO_WRITE)
        message = Message([record])

        print(f"Schreibe URL: {URL_TO_WRITE}")
        
        # Schreibe die NDEF-Nachricht auf den Tag
        tag.ndef.write(message)
        print("✅ Schreiben erfolgreich.")

    except Exception as e:
        print(f"❌ Fehler beim Schreiben: {e}", file=sys.stderr)

def main():
    # Der Context-Manager nfc.ContactlessFrontend sucht nach dem Reader
    with nfc.ContactlessFrontend('usb') as clf:
        if not clf:
            print("❌ NFC-Reader (ACR122U) nicht gefunden.")
            return

        print("NFC Reader gefunden. Halten Sie einen leeren/beschreibbaren Tag an den Reader...")
        
        # Warte, bis ein Tag erkannt wird
        # 'tt1' ist der Standard-Type (ISO 14443-3A)
        clf.connect(rdwr={'on-connect': write_tag})

if __name__ == '__main__':
    main()
