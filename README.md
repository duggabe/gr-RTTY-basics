# gr-RTTY-basics

Basic radioteletype transmit and receive functions

## Overview

This package contains GNU Radio flowgraphs for a RTTY transmitter and a RTTY receiver. They work in conjunction with [gr-webserver](https://github.com/duggabe/gr-webserver) which provides a user screen with keyboard input and display output. Whatever is typed on the keyboard is sent by the RTTY transmitter. Whatever is received by the RTTY receiver is displayed on the screen in a scrolling area showing the last 20 lines.

The package uses three separate processes: (a) RTTY transmitter, (b) RTTY receiver, and (c) gr-webserver terminal.  They all can be on the same computer or on two or more separate computers by adjusting the ZMQ socket addresses. See [ZMQ PUB Sink](https://wiki.gnuradio.org/index.php/ZMQ_PUB_Sink#Parameters) for an explanation of Addresses.

Updates have been made for the filters in the flowgraphs. They have been tested on GNU Radio versions 3.8.4.0, 3.9, and 3.10.0.0. See [Porting Existing Flowgraphs to a Newer Version](https://wiki.gnuradio.org/index.php/Porting_Existing_Flowgraphs_to_a_Newer_Version) for differences in versions.

An Eye Sink display has been added to the RTTY receiver to aid in tuning. When correctly tuned, the eye pattern will cross at the zero axis.

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

Go to [gr-webserver](https://github.com/duggabe/gr-webserver) and follow the instructions to install and start it using a separate terminal screen. **Note:** Use the current version (v2.1 or later, the `master` branch). The flowgraphs use ZMQ SUB Message Source and ZMQ PUB Message Sink blocks to match it.

## Operation

### RTTY transmitter

There are three programs to transmit RTTY:

* one for audio output - `RTTY_vco`
* one for direct USRP output - `RTTY_xmt`
* one for sending continuous LTRS characters for tuning - `RTTY_test_ltrs`.

The instructions below are for `RTTY_vco`, the audio output version, but they all operate in the same manner.

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

### RTL-SDR RTTY receiver

`RTL_SDR_RTTY_rcv` receives RTTY over the air with an RTL-SDR dongle instead of audio from a
radio. It shows the decoded text in its own window, in a box labeled "RTTY RX", so it does
not need gr-webserver.

Requirements:

* An RTL-SDR that can receive HF in direct-sampling mode. The flowgraph opens it with
  `rtl=0,direct_samp=2` (Q branch), as used by the RTL-SDR Blog V3 and V4.
* GNU Radio 3.10 with the Soapy blocks (`gr-soapy`) and the SoapyRTLSDR driver.

To run it:

1. Go to the gr-RTTY-basics/RTTY_rcv folder and start GNU Radio Companion.  
```
cd ~/gr-RTTY-basics/RTTY_rcv
gnuradio-companion
```
2. Open RTL_SDR_RTTY_rcv.grc from the file menu.
3. Click 'Run' and 'Execute' or press F6.
4. In the "RTL_SDR_RTTY_rcv" window, enter the **Receive Freq** in Hz. The flowgraph
   decodes the signal centered at Receive Freq plus the **Center freq** slider, which
   starts at -2210 Hz. That is the same as an LSB receiver with 2125/2295 Hz tones, so
   for an AFSK signal sent in LSB, enter the transmitting radio's dial frequency.
   The waterfall shows 6 kHz around the decoded signal, centered on zero. Move the Center
   freq slider (in 10 Hz steps) until the mark and space tones sit evenly either side of
   zero.
5. Adjust **Quad Demod** until the eye pattern is open and crosses at the zero axis.
   The RTL-SDR gain is fixed at 20 dB in the flowgraph.
6. Leave **Normal** selected for standard RTTY; an IC-7300 LSB-D signal from gr-icom7300
   decodes on Normal. If the text is garbled, click **Reverse**.

Decoded text appears in the "RTTY RX" box. A line is shown when a line feed arrives, or at
the next space after 80 characters.

The settings are 45.45 baud and 170 Hz shift. The signal is taken at 1.92 MS/s, shifted and
reduced to 48 kS/s (shown on the waterfall at 6 kS/s), then 960 S/s. It is FM-demodulated
and resampled to 500 S/s (11 samples per bit) for the decoder.

**Caution:** to receive a transmitter on your own bench, even into a dummy load, put an
attenuator (30 dB, for example) at the RTL-SDR input and use low transmit power. Never
connect the RTL-SDR to a transmitter output.

### Testing

There are three tests which can be done: Loop-back, over-the-air, and online RTTY news.

#### Loop-back test

Using `RTTY_vco`, if you connect the audio output of the transmitter to the audio input of the receiver using a patch cable, you can perform a loop-back test. Whatever you type in the gr-webserver screen will be displayed as received, preceeded by a less-than sign, in all capital letters. There will be a delay in the response.

#### Over-the-air test

With `RTL_SDR_RTTY_rcv` you can decode a real RTTY signal, such as a contest station, the
W1AW bulletins, or your own transmitter into a dummy load. It decoded RTTY sent from an
Icom IC-7300MK2 in LSB-D with [gr-icom7300](https://github.com/duggabe/gr-icom7300).

#### Online RTTY news

If you connect the audio output of the computer to the audio input of the receiver using a patch cable, you can go to http://internet-tty.net:8000/ITTY and start the input. You must select the 'Reverse' tones. A RTTY news feed will be displayed.


## Troubleshooting

gr-webserver publishes keyboard text on port 50251. The transmitter's ZMQ SUB Message Source connects to it. The receiver's ZMQ PUB Message Sink binds port 50252, and gr-webserver connects to it to get the text it displays.

If received text doesn't appear on the gr-webserver screen, open `http://localhost:50250/trace` in another browser tab. The current gr-webserver (`master`) logs a timestamped line there, and in its terminal, each time that connection changes:

```
13:06:37 zmq SUB connected to flowgraph
13:20:12 zmq SUB disconnected (flowgraph stopped?)
```

If `RTTY_receive` is running but the last line is `disconnected`, with no `connected` after it, restart gr-webserver: press Ctrl-C in its terminal, then run `node index.js` again. This happened once with Node.js 24 and zeromq 6.8; the cause is not known.
