#include <SPI.h>
#include <MFRC522.h>

constexpr uint8_t RST_PIN = D3; // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D4; // Configurable, see typical pin layout above

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
String tag;

const int available_workers_count = 1;
String available_workers_uids[available_workers_count] = {"22755183"};

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
}

void loop() {
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if (rfid.PICC_ReadCardSerial()) {
    for (byte i = 0; i < 4; i++) {
      tag += rfid.uid.uidByte[i];
    }
    
    validate_worker(tag);
    
    tag = "";
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}

void validate_worker(String tag) {
  for (int worker_id = 0; worker_id < available_workers_count; worker_id++) {
    // ACCESS GRANTED
    if (tag == available_workers_uids[worker_id]) { 
      send_data_to_pyton(tag);
    }
  }
}

void send_data_to_pyton(String tag) {
  if (!Serial.available()) {
    // Send tag to Serial, so we can get it in Python code
    Serial.println(tag);
  }
}
