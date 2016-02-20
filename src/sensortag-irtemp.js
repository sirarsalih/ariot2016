
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
     console.log('enable sensors');
     
	 tag.enableMagnetometer(notifyMagnetometer);
	 tag.enableIrTemperature(notifyTemp);
	 tag.enableAccelerometer(notifyAccelerometer);
	 tag.enableHumidity(notifyHumidty);
	 tag.enableMagnetometer(notifyMagnetometer);
	 tag.enableBarometricPressure(notifyBarometricPressure);
	 tag.enableGyroscope(notifyGyroscope);
	 tag.enableLuxometer(notifyLuxometer);
   }
   
   function notifyLuxometer() {
			tag.notifyLuxometer(readLuxometer);
	}
   
   function readLuxometer() {
		tag.on('luxometerChange', function(lux) {
		 console.log('\tLux = %d', lux.toFixed(1));
		 var usersRef = ref.child("luxometer");
		 usersRef.push({
			 lux: lux.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}
   
   function notifyGyroscope() {
			tag.notifyGyroscope(readGyroscope);
	}
	
	function readGyroscope() {
		tag.on('gyroscopeChange', function(x, y, z) {
		 console.log('\tx = %d', x.toFixed(1));
	     console.log('\ty = %d', y.toFixed(1));
		 console.log('\tz = %d', z.toFixed(1));
	
		 var usersRef = ref.child("gyroscope");
		 usersRef.push({
			 x: x.toFixed(1),
			 y: y.toFixed(1),
			 z: z.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}
   
   function notifyBarometricPressure() {
			tag.notifyBarometricPressure(readBarometricPressure);
	}
   
   function readBarometricPressure() {
		tag.on('barometricPressureChange', function(pressure) {
		 console.log('\tPressure = %d', pressure.toFixed(1));
		 var usersRef = ref.child("barometricpressure");
		 usersRef.push({
			 pressure: pressure.toFixed(1),
			 dateTime: new Date().toString()
		 });	 
	   });
	}
   
   function notifyMagnetometer() {
			tag.notifyMagnetometer(readMagnetometer);
	}

	function readMagnetometer() {
		tag.on('magnetometerChange', function(x, y, z) {
		 console.log('\tx = %d', x.toFixed(1));
	     console.log('\ty = %d', y.toFixed(1));
		 console.log('\tz = %d', z.toFixed(1));
		 x = x.toFixed(1);
		 y = y.toFixed(1);
		 var direction = 0.0;
		if(y>0)
			direction = 90 - [Math.atan(x/y)]*(180/3.14);
		if(y<0)
			direction = 270 - [Math.atan(x/y)] * (180/3.14);
		if(y == 0 && x<0)
			direction = 180.0;
		console.log("direction " + direction);
		console.log(headingToString2(direction))
		 var usersRef = ref.child("magnetometer");
		 usersRef.push({
			 x: x,
			 y: y,
			 z: z.toFixed(1),
			 direction: direction,
			 dateTime: new Date().toString()
		 });	 
	   });
	}
	function headingToString2(x)
	{
		var directions = {"N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"};
		return directions[Math.round((  (x % 360) / 45)) ];
	}

	function notifyHumidty() {
			tag.notifyHumidity(readHumidty);
	}

	function readHumidty() {
		tag.on('humidityChange', function(temperature, humidity) {
		 console.log('\tTemperature = %d deg. C', temperature.toFixed(1));
	     console.log('\tHumidty = %d', humidity.toFixed(1));
		 var usersRef = ref.child("humidity");
		 usersRef.push({
			 temperature: temperature.toFixed(1),
			 humidity: humidity.toFixed(1),
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