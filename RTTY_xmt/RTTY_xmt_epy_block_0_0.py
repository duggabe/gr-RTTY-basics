"""
Baudot code vector source
"""

import numpy as np
from gnuradio import gr

import pmt

ITA2 = [ 0x00, 'E', '\n', 'A', ' ', 'S', 'I', 'U', '\r', 'D', 'R', 'J', 'N', 'F', 'C', 'K',
            'T', 'Z', 'L', 'W', 'H', 'Y', 'P', 'Q', 'O', 'B', 'G', 0x0e, 'M', 'X', 'V', 0x0f,
            0x00, '3', '\n', '-', ' ', 0x07, '8', '7', '\r', '$', '4', '\'', ',', '!', ':', '(',
            '5', '\"', ')', '2', '#', '6', '0', '1', '9', '?', '&', 0x0e, '.', '/', ';', 0x0f ]

textboxValue = ""
_figs = 0x1b
_ltrs = 0x1f
_shift = 0
bit_stream = []
CQita2 =  []

class mc_sync_block(gr.sync_block):
    """
    reads input from a message port
    generates a vector of Baudot code bits
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name = "Baudot code vector source",
            in_sig = None,
            out_sig = [np.byte])
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('clear_input'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    def handle_msg(self, msg):
        global textboxValue
        textboxValue = pmt.symbol_to_string (msg)
        # print (textboxValue)
    
    def work(self, input_items, output_items):
        global ITA2
        global textboxValue
        global _figs
        global _ltrs
        global _shift
        global bit_stream
        global CQita2

#       convert UTF-8 to ITA2 (Baudot)
        if (len (textboxValue) > 0):
            bit_stream = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
            CQita2 = [31, 31]    # LTRS
            _shift = 0
            for in0 in textboxValue:
                # get next char
                inChar = str (in0)
                # convert to upper case
                ch = inChar.upper()
                # test for character in ITA2
                if (ch in ITA2):
                    _idx = ITA2.index (ch)
#                   if (not space)
                    if (ch != ' '):
#                       if index > 31       // figures
                        if (_idx > 31):
                            if (_shift == 0):
                                CQita2.append (0x1b)    # send 'figures' code
                                _shift = 0x20
                        else:                    # letters
                            if (_shift > 0):
                                CQita2.append (0x1f)     # send 'letters' code
                                _shift = 0
#                   store ITA2 char
                    _idx &= 0x1F
                    CQita2.append (int(_idx))
                else:
                    CQita2.append (4)    # space
            CQita2.append (8)    # CR
            CQita2.append (8)    # CR
            CQita2.append (2)    # LF
#            print ("CQita2:")
#            print (CQita2)

#           serialize data LSB first
            for _out in CQita2:
                outDat = _out
                _bit_count = 0
                while _bit_count < 8:
                    if (_bit_count == 0):
                        bit_stream.append (int(0))    # start bit
                    elif (_bit_count > 5):
                        bit_stream.append (int(1))    # stop bits
                    else:
                        bit_stream.append (int(outDat & 1))
                        outDat >>= 1
                    _bit_count += 1
#            print ("bit_stream:")
#            print (bit_stream)

            # get length of string
            _num_elem = len(bit_stream)
#            print ("num elements = ", _num_elem)

            # copy bit_stream to output array
            for x in range (_num_elem):
                output_items[0][x] = bit_stream[x]

            # clear input line
            textboxValue = ""
            self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
        else:
            _num_elem = 0

        return (_num_elem)
