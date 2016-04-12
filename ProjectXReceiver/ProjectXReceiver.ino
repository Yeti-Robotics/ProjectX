#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>
#include <DualVNH5019MotorShield.h>

//90-a2-da-0f-25-E7
byte mac[] = {0x90, 0xA2, 0xDA, 0x0f, 0x25, 0xE7};

//ip Address for shield
byte ip[] = {192,168,1,113};

//Use port 23 for telnet
EthernetServer server = EthernetServer(23);

//Motor shield
DualVNH5019MotorShield md;

void setup() {
	// put your setup code here, to run once:
	Serial.begin(9600);     //For visual feedback on what's going on
	while(!Serial){}

	Ethernet.begin(mac,ip); // init EthernetShield
	delay(1000);

	server.begin();
	if(server.available()){
		Serial.println("Client available");
	}

  md.init();
}

void loop() {
	EthernetClient client = server.available();
	if(client) {
	  char message = client.read();
    Serial.println("Client Message" + message);
    Serial.println(message);
    if(message & 128) {
      md.setM1Speed(message & 127);
    } else {
      md.setM2Speed(message & 127);
    }
	}
}
