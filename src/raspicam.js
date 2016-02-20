var RaspiCam = require("raspicam");
var Process = require('process');
var Firebase = require('firebase');
var ref = new Firebase("https://ariot2016.firebaseio.com/", Process.env["FIREBASE_TOKEN"]);
var fs = require('fs');
var camera = new RaspiCam({
	mode: "photo",
	output: "./photo/image.jpg",
	encoding: "jpg",
	timeout: 0 // take the picture immediately
});

setInterval(function(){ 
       camera.on("started", function( err, timestamp ){
		console.log("photo started at " + timestamp );
	});
	
	camera.on("read", function( err, timestamp, filename ){
		console.log("photo image captured with filename: " + filename );
	});
	
	camera.on("exit", function( timestamp ){
		console.log("photo child process has exited at " + timestamp );
	});
	
	camera.start();
	
	function base64_encode(file) {
		var bitmap = fs.readFileSync(file);
		return new Buffer(bitmap).toString('base64');
	}
	
	function base64_decode(base64str, file) {
		var bitmap = new Buffer(base64str, 'base64');
		fs.writeFileSync(file, bitmap);
		console.log('******** File created from base64 encoded string ********');
	}
	
	var base64str = base64_encode('photo/image.jpg');
	//base64_decode(base64str, 'copy.jpg');
	
	var vsRef = ref.child("pictures");
	vsRef.push({
				dateTime: new Date().toString(),
				base64: base64str
			});
			console.log("Pushed base64 to FireBase...")
}, 1000);

