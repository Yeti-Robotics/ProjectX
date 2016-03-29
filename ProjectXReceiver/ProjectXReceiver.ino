#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>
#include <DualVNH5019MotorShield.h>

/90-a2-da-0f-25-E7
byte mac[] = {0x90, 0xA2, 0xDA, 0x0f, 0x25, 0xE7};

//ip Address for shield
byte ip[] = {192,168,1,113};

//Use port 23 for telnet
EthernetServer server = EthernetServer(23);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);     //For visual feedback on what's going on
  while(!Serial){
    ;   //wait for serial to connect -- needed by Leonardo
  }

  Ethernet.begin(mac,ip); // init EthernetShield
  delay(1000);

  server.begin();
  if(server.available()){
    Serial.println("Client available");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  EthernetClient client = server.available();
  message = client.read();

  server.write(message);
  server.write("Testu ");
  Serial.println(message);

//  if (client == true){                    <----- This check screwed it up. Not needed.
//    Serial.println("Client Connected.");
//    server.write(client.read());        //send back to the client whatever     the client sent to us.
//  }
}
