var Firebase = require('firebase');
var ref = new Firebase("https://ariot2016.firebaseio.com/");
var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var vsRef = ref.child("videostream");		 
var videoStream = client.getVideoStream();
videoStream.on('data', vsRef.push({
			 stream: console.log			 
		 }));
