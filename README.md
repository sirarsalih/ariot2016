<h1>Arctic IoT Challenge 2016</h1>

<h2>Raiders of the Lost Pi</h2>

<h3>The Concept</h3>

In a tunnel or a mine shaft, an accident can potentially cause very dangerous situations and even fatalities. The time from a collision to the situation is under control is critical. The first thing an accident responder team will have to do is map out the situation. In a tunnel, gases and fire can prevent a team from going into the tunnel. Dangerous gases from a fire can behave differently in a tunnel because of chemical properties, some rising and others sinking.

Norway has a lot of long tunnels, some over 20 kilometers. Connectivity in a tunnel is, as we all know, usually not very good. Laying out internet connection to cover the whole tunnel might be very costly.

Our solution: <strong>Tunnel Raiders</strong>

<h3>The Solution</h3>

Tunnel Raiders are Parrot AR Drones, the idea is to control the drones through the internet using a Raspberry Pi 2 and performing REST calls, the drones are equipped with various sensors to analyze the tunnels. A <a href="http://expressjs.com/" target="_blank">Node.js Express</a> server for the <a href="http://ardrone2.parrot.com/" target="_blank">Parrot AR Drone 2.0</a>. The server uses the <a href="https://github.com/felixge/node-ar-drone" target="_blank">node-ar-drone</a> and <a href="https://github.com/eschnou/ardrone-autonomy" target="_blank">ardrone-autonomy</a> libraries to fly the drone with REST calls.

<h4>Getting Started</h4>

1. SSH into a Raspberry Pi and clone this repository.
2. Download and install <a href="http://nodejs.org/download/" target="_blank">Node.js</a>. 
3. Start up cmd or terminal and execute the following command:
<p><code>npm install</code></p>

This installs the following framework and libraries:

- <a href="http://expressjs.com/" target="_blank">Express</a> framework, which is a lightweight version of Node.js.
- <a href="http://nodemon.io/" target="_blank">nodemon</a>, which monitors changes in the server source code and automatically restarts the server.
- <a href="https://github.com/felixge/node-ar-drone" target="_blank">node-ar-drone</a> library: This library is used to fly the drone.
- <a href="https://github.com/eschnou/ardrone-autonomy" target="_blank">ardrone-autonomy</a> library: This library helps us automate the drone, for instance, enabling us to send predefined flying coordinates.

4. Run install.sh.

<strong>PS: All the steps above are run on the Raspberry Pi device, through SSH.</strong>

<h4>Connecting to the Drone through a Raspberry Pi using SSH</h4>

Once the drone is turned on, it will send out WiFi signals like a router. Connect your Pi to the drone via WiFi. Like a router, the drone uses the IP <code>192.168.1.1</code> by default.

Start up an SSH shell, connect to the Pi, navigate to <code>repl.js</code> and execute the following command:
<p><code>nodemon repl.js</code></p> 
This establishes a connection to the (default) IP of the drone at <code>192.168.1.1</code>. While connected to the drone, in terminal, execute the following command:
<p><code>takeoff()</code></p>
This takes off the drone, and it will start hovering in the air. Land the drone by executing the following command:
<p><code>land()</code></p>
There are many other commands you can experiment with, more information provided <a href="https://github.com/felixge/node-ar-drone" target="_blank">here</a>.

<h4>Flying the Drone with REST Calls</h4>

Now that we are able to establish a connection to the drone and test fly it, we are now ready to control it with REST calls using Node.js. Start up cmd or terminal and navigate to <code>node_server.js</code>, then execute the following command:
<p><code>nodemon node_server.js</code></p>
This establishes a connection to the drone and starts up a local express Node.js server at port <code>1337</code>. As you can see in <code>node_server.js</code>, we have defined serveral GET requests. Start up your browser and go to <a href="http://localhost:1337" target="_blank">http://localhost:1337</a>, you should be greeted by the message <code>Welcome to my Parrot AR node server!</code>

Try to control the drone by sending GET requests to your local Node.js server:

<ul>
<li><code>http://localhost:1337/takeoff</code> takes off the drone, starts hovering it for 5 seconds and then lands it.</li>
<li><code>http://localhost:1337/takeoffAndSpin</code> takes off the drone, starts hovering it for 4 seconds, spins it clockwise and then lands it after 1 second.</li>
<li><code>http://localhost:1337/land</code> lands the drone immediately.</li>
</ul>

<h4>Automating the Drone Flight Path (NOT SAFE)</h4>

We can also automate the flight path of the drone, by providing predefined <code>x,y</code> coordinates. You can do this by doing a call to <code>http://localhost:1337/takeoffAndFly</code> and then appending the call with the coordinates. Here is an example:

<ul>
<li>
<code>http://localhost:1337/takeoffAndFly?c=8,5&c=4,5</code> takes off the drone, flies it to <code>x,y</code> coordinates <code>[8,5]</code>, <code>[4,5]</code> and then lands it. 
</li>
</ul>
