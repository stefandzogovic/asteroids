		ASTEROIDS PROJECT
----------------------------------------------------
- Created by: Aleksandar Popovic, Stefan Dzogovic,
	      Luka Draca and Ilija Marinovic

		Project Description
----------------------------------------------------

-Clone of Atari's 1979 game written in Python 3.8.

-Technologies used: Python 3.8, PyQt5(5.14.1), 
		    PyQt5-sip (12.7.0), pip(19.0.3),
		    setup-tools(40.8.0)

		Game Description
----------------------------------------------------

SINGLE PLAYER:

- Game starts when the user runs Menu.py file.
- Starting menu appears where the user can choose 
  between 3 options (Play, Tournament, Quit).
- Player then chooses his avatar.
- Game has begun and depending on the choice of avatar, 
  Score, Lives, Waves and Levels are in the color 
  of the chosen avatar.
- Player is a spaceship and enemies are asteroids.
- When user presses UP, LEFT, RIGHT, SPACE, on keyboard,
  player moves up, left, right and fires an missile.
- With a missile player destroys asteroids which
  increases his score
- Each level has waves of asteroids which number 
  equals to the number of the current level
- After each level, number of asteroids are increased
  by one, speed of player and asteroids are also 
  increased.
- Game lasts until the player loses all lives
- Deus Ex Machina object can spawn on the screen
  which when picked up can grant the player a life or
  can slow down the player for 8 seconds.

MULTIPLAYER:

- Every user needs to disable their Domain and Public
  Firewalls to be able to run this program.
- server1.py needs to be run only once on a single 
  PC
- Every user who wants to play the game need to change
  self.host field of network.py file
  to the ipv4 address of PC who runs the server.
  example ('192.168.3.14')
- After the server1.py file is run, players have X
  seconds to run game1.py file to connect to the game
- After X seconds the game has begun

		       BUGS  
-----------------------------------------------------
- Missile can be stuck in field after colliding with
  an asteroid.
- Multiplayer not finished.


