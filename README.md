A desktop/mobile cross platform game written in python using the Kivy framework. Similar in concept to the game Avalanche (http://www.addictinggames.com/action-games/avalanche.jsp)
The aim of the game is to control a character, dodge and use falling objects to gain height. 
A high height will result in a high score. This game is an ongoing side project to develop competency and skills in python and game development. 
Will eventually be playable on mobile, making use of the device's accelerometer and multi touch capabilities.

<p float="left">
  <img src="gameArt/Screenshot.png" width="450" />
</p>

NOTES 
ImportError: no valuable window provider found
-> broken for python 3, currently using python 2.7.14
-> needed to install Cython for kivy compilation
-> needed to install kivy dependancies

Permissions denied: /dev/input/event*
- /dev/input/event is responsible for keyboard and mice input events
- adding user to 'input' group solved problem
- sudo usermod -a -G <group> <user> then re-login
- note: 'whoami' will show user name

Switch to Macbook
- Works for python3 only

