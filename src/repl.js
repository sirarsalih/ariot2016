/**
 * Created by Sirar on 18.02.2016.
 */

var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var Firebase = require('firebase');

var ref = new Firebase("https://ariot2016.firebaseio.com/", "rg142hjQO5w0mO6qIUUb1U60gkeZUL3G6fhgMFl4");

client.createRepl();
	
var statusData = {
    'height': client._lastAltitude,
    'battery': client._lastBattery,
    'state': client._lastState,
    'lowBattery': false
};

client.on('batteryChange', function(batt) {

    statusData['battery'] = batt;
	console.log(batt);
});

setInterval(function(){ 
statusData['state'] = client._lastState;
var vsRef = ref.child("droneStatus");
console.log(statusData.height)
vsRef.push(statusData);
}, 5000);
