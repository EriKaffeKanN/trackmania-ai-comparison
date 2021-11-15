#name "Game Data collector"
#author "Erik Andersson"

/*CTrackManiaPlayer@ GetViewingPlayer()
{
    auto playground = GetApp().CurrentPlayground;
    if (playground is null || playground.GameTerminals.Length != 1) {
        return null;
    }
    return cast<CTrackManiaPlayer>(playground.GameTerminals[0].GUIPlayer);
}*/

class GG
{
    int a;
    GG(int g) {
        a = g;
    }
}

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


    CGameCtnApp@ app = GetApp();
    CGamePlayground@ playground = app.CurrentPlayground;
    MwFastBuffer<CGamePlayer@> players = playground.Players;
    //CTrackManiaPlayer@ player = cast<CTrackManiaPlayer@>(players[0]);
    //auto player = players[0];
    CSmPlayer@ player = cast<CSmPlayer@>(players[0]);
    CSmScriptPlayer@ sApi = player.ScriptAPI;


    print("Connected, ready to communicate");
    while(true) {
        string output = "";
        output = output + sApi.Speed; // yeah. this is horrible. but that's only because openplanet sucks and won't let me convert an int to a string properly
        sock.WriteRaw("updateGameState|" + output);
        yield();
    }
}