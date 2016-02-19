var Firebase = require('firebase');
var Process = require('process');
var ref = new Firebase("https://ariot2016.firebaseio.com/", Process.env["FIREBASE_TOKEN"]);
var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var vsRef = ref.child("videostream");		 
var videoStream = client.getPngStream();
videoStream.on('data', function(buffer) {
 vsRef.push(buffer);
});
