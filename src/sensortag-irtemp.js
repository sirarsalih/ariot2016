
var Firebase = require('firebase');
var ref = new Firebase("https://docs-examples.firebaseio.com/web/saving-data/fireblog");
var SensorTag = require('sensortag');

SensorTag.discover(function (tag) {

    tag.on('disconnect', function () {
		console.log('disconnected!');
		process.exit(0);
	});

	function connectAndSetUpTag() {			
        console.log('connectAndSetUp');
	    tag.connectAndSetUp(enableIrTemp);
	}

   function enableIrTemp() {		
     console.log('enableIRTemperatureSensor');
     // when you enable the IR Temperature sensor, start notifications:
     tag.enableIrTemperature(notifyMe);
   }

	function notifyMe() {
    	tag.notifyIrTemperature(readTemperature);   	// start the accelerometer listener
   }

	function readTemperature() {
		tag.on('irTemperatureChange', function(objectTemp, ambientTemp) {
	     console.log('\tObject Temp = %d deg. C', objectTemp.toFixed(1));
	     console.log('\tAmbient Temp = %d deg. C', ambientTemp.toFixed(1));
		 var usersRef = ref.child("temperatures");
		 usersRef.child("objectTemp").set({
			temp: objectTemp.toFixed(1),
			});
		 usersRef.child("ambientTemp").set({
			temp: ambientTemp.toFixed(1),
			});
	   });
	}

	connectAndSetUpTag();
});