import serial
import sqlite3
from datetime import datetime
import threading
import time
import sys 

class ArduinoBluetoothReceiver:
    def __init__(self, port, baudrate=9600, db_path='led_database.db'):
        """
        Inizializza il ricevitore Bluetooth
        
        Args:
            port: Porta seriale Bluetooth (es. 'COM5' su Windows, '/dev/rfcomm0' su Linux)
            baudrate: Velocità di comunicazione (default 9600)
            db_path: Percorso del database SQLite
        """
        self.port = port
        self.baudrate = baudrate
        self.db_path = db_path
        self.serial_conn = None
        self.db_conn = None
        self.running = False
        
    def setup_database(self):
        """Crea il database e le tabelle necessarie"""
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.db_conn.cursor()
        
        # Crea la tabella
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS led_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stato VARCHAR(10) NOT NULL,
                timestamp_arduino INTEGER NOT NULL,
                timestamp_sistema DATETIME DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT check_stato CHECK (stato IN ('ACCESO', 'SPENTO'))
            )
        ''')
        
        # Crea l'indice
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON led_events(timestamp_sistema)
        ''')
        
        self.db_conn.commit()
        print(f"Database '{self.db_path}' configurato correttamente")
        
    def connect_bluetooth(self):
        """Stabilisce la connessione Bluetooth"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connesso a {self.port} a {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"Errore di connessione: {e}")
            return False
            
    def parse_message(self, message):
        """
        Analizza il messaggio ricevuto dall'Arduino
        Formato atteso: LED_STATE:ACCESO:timestamp o LED_STATE:SPENTO:timestamp
        """
        try:
            parts = message.strip().split(':')
            if len(parts) == 3 and parts[0] == 'LED_STATE':
                stato = parts[1]
                timestamp_arduino = int(parts[2])
                return stato, timestamp_arduino
        except (ValueError, IndexError):
            pass
        return None, None
        
    def save_to_database(self, stato, timestamp_arduino):
        """Salva l'evento nel database"""
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO led_events (stato, timestamp_arduino) 
            VALUES (?, ?)
        ''', (stato, timestamp_arduino))
        self.db_conn.commit()
        
        # Recupera l'ID dell'ultimo inserimento
        event_id = cursor.lastrowid
        timestamp_sistema = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{timestamp_sistema}] Salvato: LED {stato} (ID: {event_id})")
        
    def print_statistics(self):
        """Stampa statistiche dal database"""
        cursor = self.db_conn.cursor()
        
        # Conta eventi per stato
        cursor.execute('SELECT stato, COUNT(*) FROM led_events GROUP BY stato')
        stats = cursor.fetchall()
        
        print("\n--- STATISTICHE ---")
        for stato, count in stats:
            print(f"LED {stato}: {count} volte")
            
        # Ultimi 5 eventi
        cursor.execute('''
            SELECT stato, timestamp_sistema 
            FROM led_events 
            ORDER BY timestamp_sistema DESC 
            LIMIT 5
        ''')
        recent = cursor.fetchall()
        
        print("\nUltimi 5 eventi:")
        for stato, timestamp in recent:
            print(f"  {timestamp}: LED {stato}")
        print("------------------\n")
        
    def start(self):
        """Avvia la ricezione dei dati"""
        self.setup_database()
        
        if not self.connect_bluetooth():
            return
            
        self.running = True
        print("In attesa di dati dall'Arduino...")
        print("Premi Ctrl+C per terminare\n")
        
        try:
            while self.running:
                if self.serial_conn.in_waiting > 0:
                    try:
                        # Leggi una linea
                        line = self.serial_conn.readline().decode('utf-8').strip()
                        
                        if line:
                            # Analizza il messaggio
                            stato, timestamp_arduino = self.parse_message(line)
                            
                            if stato and timestamp_arduino:
                                # Salva nel database
                                self.save_to_database(stato, timestamp_arduino)
                                
                                # Mostra statistiche ogni 10 eventi
                                cursor = self.db_conn.cursor()
                                cursor.execute('SELECT COUNT(*) FROM led_events')
                                count = cursor.fetchone()[0]
                                if count % 10 == 0:
                                    self.print_statistics()
                                    
                    except UnicodeDecodeError:
                        print("Errore di decodifica, messaggio ignorato")
                        
                time.sleep(0.01)  # Piccola pausa per non sovraccaricare la CPU
                
        except KeyboardInterrupt:
            print("\n\nInterruzione richiesta dall'utente")
        finally:
            self.stop()
            
    def stop(self):
        """Ferma la ricezione e chiude le connessioni"""
        self.running = False
        
        if self.serial_conn:
            self.serial_conn.close()
            print("Connessione Bluetooth chiusa")
            
        if self.db_conn:
            self.print_statistics()
            self.db_conn.close()
            print("Database chiuso")

def main():
    # Configurazione    
    BLUETOOTH_PORT = 'COM5'  
    
    print("=== Ricevitore Bluetooth Arduino ===")
    print(f"Porta configurata: {BLUETOOTH_PORT}")
    print("Assicurati che:")
    print("1. L'Arduino sia acceso e il Bluetooth attivo")
    print("2. Il dispositivo sia stato accoppiato con il PC")
    print("3. La porta seriale sia corretta\n")
    
    # Crea e avvia il ricevitore
    receiver = ArduinoBluetoothReceiver(
        port=BLUETOOTH_PORT,
        baudrate=9600,
        db_path='led_database.db'
    )
    
    receiver.start()

if __name__ == "__main__":
    main()