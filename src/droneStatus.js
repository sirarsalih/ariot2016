var client  = arDrone.createClient();
var Firebase = require('firebase');
var Process = require('process');

var ref = new Firebase("https://ariot2016.firebaseio.com/", Process.env["FIREBASE_TOKEN"]);

var statusData = {
    'height': client._lastAltitude,
    'battery': client._lastBattery,
    'state': client._lastState,
    'lowBattery': false
};

client.on('lowBattery', function(batt) {
    statusData['lowBattery'] = true;
});

setInterval(function(){ 
statusData['state'] = client._lastState;
var vsRef = ref.child("droneStatus");
vsRef.push(statusData);
}, 5000);
