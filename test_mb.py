#!/usr/bin/env python

import unittest
import mb_helper as mbh
import array

class ModbusTestCase(unittest.TestCase):
	"""Unit Tests for `modbus.py`."""

	mb=mbh.MBHelper()

	
	def test_connection(self):
		"""Test connection to 127.0.0.1 on port 1502"""
		self.assertTrue(self.mb.mb_connect('127.0.0.1', 1502, 500))

	def test_send_mb_data(self):
		"""Test MB Send command to 127.0.0.1 on port 1502. Register 106 must equal a value of 12.
		"""
		self.assertEqual(self.mb.mb_send_cmd('127.0.0.1', 1502, 11, 3, '00 69 00 01'), b'\x00\x00\x00\x00\x00\x05\x0b\x03\x02\x00\x0c')
   
	def test_scan_mb(self):
		"""Test MB Scan command to 127.0.0.1 on port 1502"""
		self.assertEqual(self.mb.mb_scan('127.0.0.1', 1502, 1, 130), ['127.0.0.1'])
		self.assertEqual(self.mb.mb_scan('127.0.0.1', 1502), ['127.0.0.1'])

if __name__ == '__main__':
	unittest.main()