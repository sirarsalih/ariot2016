
var Firebase = require('firebase');
var ref = new Firebase("https://ariot2016.firebaseio.com/");
var SensorTag = require('sensortag');

SensorTag.discover(function (tag) {

    tag.on('disconnect', function () {
		console.log('disconnected!');
		process.exit(0);
	});

	function connectAndSetUpTag() {			
        console.log('connectAndSetUp');
	    tag.connectAndSetUp(enableSensors);
	}
	
	function enableSensors() {		
     console.log('enableIRTemperatureSensor');
     tag.enableIrTemperature(notifyTemp);
	 tag.enableAccelerometer(notifyAccelerometer);
	 tag.enableHumidity(notifyHumidty);
   }

	function notifyHumidty() {
			tag.notifyHumidity(readHumidty);
	}

	function readHumidty() {
		tag.on('humidityChange', function(temperature, humidity) {
		 console.log('\tTemperature = %d deg. C', temperature.toFixed(1));
	     console.log('\tyHumidty = %d', humidity.toFixed(1));
		 var usersRef = ref.child("accelerometer");
		 usersRef.push({
			 x: temperature.toFixed(1),
			 y: humidity.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}   

	function notifyAccelerometer() {
			tag.notifyAccelerometer(readAccelerometer);
	}
	
	function readAccelerometer() {
		tag.on('accelerometerChange', function(x, y, z) {
		 console.log('\tx = %d', x.toFixed(1));
	     console.log('\ty = %d', y.toFixed(1));
		 console.log('\tz = %d', z.toFixed(1));
		 var usersRef = ref.child("accelerometer");
		 usersRef.push({
			 x: x.toFixed(1),
			 y: y.toFixed(1),
			 z: z.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}   

	function notifyTemp() {
    	tag.notifyIrTemperature(readTemperature); 
   }

	function readTemperature() {
		tag.on('irTemperatureChange', function(objectTemp, ambientTemp) {
	     console.log('\tObject Temp = %d deg. C', objectTemp.toFixed(1));
	     console.log('\tAmbient Temp = %d deg. C', ambientTemp.toFixed(1));
		 var usersRef = ref.child("temperatures");
		 usersRef.push({
			 objectTemp: objectTemp.toFixed(1),
			 ambientTemp: ambientTemp.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}

	connectAndSetUpTag();
});