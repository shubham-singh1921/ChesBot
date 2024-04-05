# ChesBot
chess bot extension and python (websocket,subprocess,python,stockfish)

this is a simple python script and web extension in js

* web extension sends data of board pieces to backend websocket.
* the socket pass the data to parser.
* parser convert it to positional argument and pass it to subprocess stockfish as input.
* stockfish produces a next move in text format.


	other requirments:
		chess engine: stockfish : https://stockfishchess.org/download/
   
How to Get Started:
	run the main.py: 
		python3 main.py
	
	get extension to your browser:
	for firefox:
		1: type about:debugging in search box
		2: click on this firefox
		3: click load temporary add on
		4: select manifest.json file
		
	now before starting a game:
		1: click the extension and click start;
		2: it will form a connection with backend socket
		3: it calculates moves for every x millisecond 
		4: it is capable  of calculating multiple moves so 
		
	note:
		1:atleast keep few milli second of time difference before you play another move.
		2: don't worry about opponent playing fast it can manage two moves in one cycle.
		3: output will be in text format so focus on terminal.
   
   
  
