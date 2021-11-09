#name "Game Data collector"
#author "Erik Andersson"

void Main()
{
    // Get connection details
    // TODO: Change to JSON
    string HOST = "127.0.0.1";
    int PORT = 5656;

    auto sock = Net::Socket();

    if(!sock.Connect(HOST, PORT)) {
        print("Couldn't connect to server");
        return;
    }

    print("Connecting...");

    while(!sock.CanWrite()) {
        yield();
    }

    print("Connected, ready to communicate");
    print(MwFoundations::CMwNod::CGameScriptVehicle::velocity);
    /*while(true){
        sock.WriteRaw("updateGameState|10,20");
        yield();
    }*/
}