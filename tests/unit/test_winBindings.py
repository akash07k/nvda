# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import ctypes
import importlib
import unittest
from ctypes import c_void_p
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPWSTR
from unittest import mock

from winBindings import magnification, winusb, wtsapi32


class TestUnavailableMagnification(unittest.TestCase):
	def test_bindReturnsCallableStub(self):
		with mock.patch.object(magnification, "dll", None):
			binding = magnification._bind("MissingFunction", mock.sentinel.prototype)

		self.assertIs(binding, magnification._unavailable)
		with self.assertRaisesRegex(OSError, "Magnification API is not available"):
			binding(showCursor=True)


class TestUnavailableWinUsb(unittest.TestCase):
	def test_bindReturnsCallableStub(self):
		with mock.patch.object(winusb, "dll", None):
			binding = winusb._bind("MissingFunction", (), None)

		self.assertIs(binding, winusb._unavailable)
		with self.assertRaisesRegex(OSError, "WinUSB is not available"):
			binding(buffer=None)


class TestUnavailableWtsApi32(unittest.TestCase):
	def test_importHandlesUnavailableDll(self):
		loadError = OSError("missing wtsapi32.dll")
		unavailableWindll = mock.MagicMock()
		type(unavailableWindll).wtsapi32 = mock.PropertyMock(side_effect=loadError)
		try:
			with mock.patch.object(ctypes, "windll", unavailableWindll):
				importlib.reload(wtsapi32)

			self.assertFalse(wtsapi32.WTSAPI32_AVAILABLE)
			self.assertIs(wtsapi32.WTSAPI32_LOAD_ERROR, loadError)
			self.assertIsNot(wtsapi32.WTSFreeMemory, wtsapi32.WTSQuerySessionInformation)
			self.assertEqual((c_void_p,), wtsapi32.WTSFreeMemory.argtypes)
			self.assertEqual(
				(HANDLE, DWORD, ctypes.c_int, ctypes.POINTER(LPWSTR), ctypes.POINTER(DWORD)),
				wtsapi32.WTSQuerySessionInformation.argtypes,
			)
			self.assertIs(BOOL, wtsapi32.WTSQuerySessionInformation.restype)
			with self.assertRaisesRegex(OSError, "Windows Terminal Services API is not available") as error:
				wtsapi32.WTSQuerySessionInformation()
			self.assertIs(error.exception.__cause__, loadError)
		finally:
			importlib.reload(wtsapi32)
