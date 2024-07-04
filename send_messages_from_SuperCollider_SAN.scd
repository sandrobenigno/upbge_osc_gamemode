
// 0. Set server and port
~n = NetAddr("127.0.0.1", 9999);//sending port

// 1. Run a routine to move the object by name:
(
~t1 = Routine({
	var timewait, command;
	inf.do({
		command = [
			["/move","MyCube_Jackson", rrand(-0.2,0.2), rrand(-0.2,0.2), 0],
			["/rotate","MyCube_Jackson", 0,0, rrand(-3,3)*90]
		].choose;
		timewait = rrand(0.2,0.5);
		~n.sendMsg(*command);
		timewait.wait;
	});
}).play();
)

// 2. Stop the routine
~t1.stop();

// 3. Play some actions (animations)
~n.sendMsg("/play","MyCube_Jackson","Jump");
~n.sendMsg("/play","MyCube_Jackson","Spin");

// 3. Stop the server and quit the game
~n.sendMsg("/quit",1);

