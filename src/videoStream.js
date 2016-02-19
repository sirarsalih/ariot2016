var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var videoStream = client.getVideoStream();
videoStream.on('data', console.log);
