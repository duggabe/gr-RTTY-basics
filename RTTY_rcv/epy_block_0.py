"""
Terminal Display Sink
"""

#  epy_block_0.py
#  revised 07/07/2019

import numpy as np
from gnuradio import gr
import pmt

ITA2 = [ '\x00', 'E', '\n', 'A', ' ', 'S', 'I', 'U', '\r', 'D', 'R', 'J', 'N', 'F', 'C', 'K',
            'T', 'Z', 'L', 'W', 'H', 'Y', 'P', 'Q', 'O', 'B', 'G', '\x0e', 'M', 'X', 'V', '\x0f',
            '\x00', '3', '\n', '-', ' ', '\x07', '8', '7', '\r', '$', '4', '\'', ',', '!', ':', '(',
            '5', '\"', ')', '2', '#', '6', '0', '1', '9', '?', '&', '\x0e', '.', '/', ';', '\x0f' ]


_samples = [ 11, 22, 33, 44, 55, 66, 77 ]
_in_sync = 0
_bit_count = 0	# actually sample count from beginning of start bit
_num_ones = 0
_num_zeros = 0
_byte = 0	# this is the index into ITA2
_in_bit = 0
_shift = 0
outLine = []
outCount = 0

class my_sync_block(gr.sync_block):
    """
	reads stream of 1's and 0's
	there are 11 samples for each bit time
	synchronizes on start bit
	uses majority of samples in a bit to determine validity
	creates Baudot character
	converts Baudot to UTF-8
	displays characters on terminal screen
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name = "Terminal Display Sink",
            in_sig = [np.byte],
            out_sig = None)
        self.message_port_register_out(pmt.intern('msg_out'))

    def work(self, input_items, output_items):
        global _samples
        global _in_sync
        global _bit_count
        global _num_ones
        global _num_zeros
        global _byte
        global _in_bit
        global _shift
        global outLine
        global outCount

        for ch in input_items[0]:
            if (ch == 1):
                _num_ones += 1       # count ones in this symbol time
            else:
                _num_zeros += 1      # count zeros in this symbol time
            _bit_count += 1          # count from first start bit after syncing
            if (_in_sync == 0):
                if (ch == 0):
                    _in_sync = 1
                    _bit_count = 1
                    _num_ones = 0
                    _num_zeros = 1
                    _byte = 0
                    # print ("sync")

            if (_bit_count in _samples) and (_in_sync == 1):    # end of this symbol time
                if (_num_ones > 7):
                    _in_bit = 1
                elif (_num_zeros > 7):
                    _in_bit = 0
                else:
                    _in_bit = -1
                    _in_sync = 0    # lots of noise
                # print ("_in_sync", _in_sync)
                # print ("_bit_count", _bit_count)
                # print ("_num_ones", _num_ones)
                # print ("_num_zeros", _num_zeros)
                _num_ones = 0
                _num_zeros = 0

                if (_in_sync == 1) and (_bit_count < 77):
                    _byte >>= 1
                    if (_in_bit == 1):
                        _byte += 16
                    # print (_byte)

                if (_in_sync == 1) and (_bit_count == 77):
                    if (_byte > 0) and (_byte < 64):
                        _byte += _shift
                        if ((_byte == 0x1b) or (_byte == 0x3b)):        # shift out (figs)
                            _shift = 0x20
                        elif ((_byte == 0x1f) or (_byte == 0x3f)):        # shift in (ltrs)
                            _shift = 0
                        else:
                            if ((_byte != 2) and (_byte != 34)):
                                outLine.append (ITA2[_byte])
                    else:
                        outLine.append ('*')
                    _num_ones = 0
                    _num_zeros = 0
                    _in_sync = 0
                    _bit_count = 0
                    outCount += 1
                    if ((outCount > 80) and (ITA2[_byte] == ' ')) or (_byte == 2) or (_byte == 34):  # LF
                        dispLine = "".join (outLine)
                        self.message_port_pub (pmt.intern('msg_out'), pmt.intern (dispLine))
                        outLine = []
                        outCount = 0

        return len(input_items[0])

