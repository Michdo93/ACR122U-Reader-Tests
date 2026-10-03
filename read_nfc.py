import nfc
import sys
from nfc.ndef import Message

def read_tag(tag):
    """Liest die NDEF-Nachricht vom Tag."""
    try:
        if not tag.ndef:
            print("Tag gefunden, aber keine NDEF-Nachricht vorhanden.")
            return

        # Lese die NDEF-Nachricht
        message = tag.ndef.message
        
        print("✅ Tag erfolgreich gelesen.")
        print("-" * 30)
        
        # Gib jeden Record in der Nachricht aus
        for record in message:
            print(f"Record Typ: {record.type.decode()}")
            # Versuche, den Payload als Text oder URI zu dekodieren
            try:
                # payload[3:] entfernt den Status-Byte und die Längen-Bytes für URIs
                data = record.payload.decode('utf-8', errors='ignore').strip()
                print(f"Inhalt: {data}")
            except:
                print(f"Inhalt (Rohdaten): {record.payload}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ Fehler beim Lesen: {e}", file=sys.stderr)

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        if not clf:
            print("❌ NFC-Reader (ACR122U) nicht gefunden.")
            return

        print("NFC Reader gefunden. Halten Sie einen NFC-Tag an den Reader...")
        
        # Warte, bis ein Tag erkannt wird und führe read_tag aus
        clf.connect(rdwr={'on-connect': read_tag})

if __name__ == '__main__':
    main()
