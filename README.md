# gr-RTTY-basics

Basic radioteletype transmit and receive functions

## Overview

This package contains GNU Radio flowgraphs for a RTTY transmitter and a RTTY receiver. They work in conjunction with [gr-webserver](https://github.com/duggabe/gr-webserver) which provides a user screen with keyboard input and display output. Whatever is typed on the keyboard is sent by the RTTY transmitter. Whatever is received by the RTTY receiver is displayed on the screen in a scrolling area showing the last 20 lines.

The package uses three separate processes. They can all be on the same computer or on two or three separate computers as the user sees fit. It has been tested on GNU Radio versions 3.8.1.0 and 3.9 pre-release.

## Installation

See [What is GNU Radio?](https://wiki.gnuradio.org/index.php/What_is_GNU_Radio%3F) and [Installing GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR) for background information.

### gr-RTTY-basics

Note: These instructions are written for a Linux OS. Similar commands work for Mac and Windows.

1. Open a terminal window.
2. Change to the home directory.  
```
cd ~/  
```
3. If you don't have 'git', enter  
```
sudo apt install git  
```
4. Clone the repository:  
```
git clone https://github.com/duggabe/gr-RTTY-basics.git
```

### gr-webserver

Go to [gr-webserver](https://github.com/duggabe/gr-webserver) and follow the instructions to install and start it using a separate terminal screen.

## Operation

### RTTY transmitter

1. Open a terminal window.
2. Go to the gr-RTTY-basics/RTTY_xmt folder.  
```
cd ~/gr-RTTY-basics/RTTY_xmt
```
3. Execute Gnu Radio Companion.  
```
gnuradio-companion
```
4. Open RTTY_vco.grc from the file menu.
5. Click 'Run' and 'Execute' or press F6.
6. A new window titled "RTTY_vco" will open showing a scope trace with the transmitted signal.
7. To Terminate the program, click the 'x' in the corner of the title line.


### RTTY receiver

1. Open a terminal window.
2. Go to the gr-RTTY-basics/RTTY_rcv folder.  
```
cd ~/gr-RTTY-basics/RTTY_rcv
```
3. Execute Gnu Radio Companion.  
```
gnuradio-companion
```
4. Open RTTY_receive.grc from the file menu.
5. Click 'Run' and 'Execute' or press F6.
6. A new window titled "RTTY_receive" will open showing a chooser block with 'Normal' and 'Reverse'. If the received signal has reversed Mark and Space tones, click the 'Reverse' button. A scope trace shows the received signal.

### Loop-back test

If you connect the audio output of the transmitter to the audio input of the receiver using a patch cable, you can perform a loop-back test. Whatever you type in the gr-webserver screen will be displayed as received, preceeded by a less-than sign, in all capital letters. There will be a delay in the response.

