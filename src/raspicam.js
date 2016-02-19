var cameraOptions = {
    width       : 600,
    height      : 338,
    mode        : "timelapse",
    awb         : 'cloud',
    output      : 'images/picture.jpg',
    q           : 50,
    rot         : 270,
    nopreview   : true,
    timeout     : 1000,
    timelapse   : 9999,
    th          : "0:0:0"
};
 
var camera = new require("raspicam")(cameraOptions);

camera.start();