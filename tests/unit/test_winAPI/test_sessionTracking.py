# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

from winAPI import sessionTracking
from winAPI._wtsApi32 import WTS_LockState


class TestIsWindowsLockedCheckViaSessionQuery(unittest.TestCase):
	def test_unknownLockState_inWinPE_isTreatedAsUnlockedWithoutAnError(self):
		with (
			mock.patch.object(
				sessionTracking,
				"_getSessionLockedValue",
				return_value=WTS_LockState.WTS_SESSIONSTATE_UNKNOWN,
			),
			mock.patch.object(sessionTracking.winVersion, "isRunningInWinPE", return_value=True),
			mock.patch.object(sessionTracking.log, "debug") as logDebug,
			mock.patch.object(sessionTracking.log, "error") as logError,
		):
			isLocked = sessionTracking._isWindowsLocked_checkViaSessionQuery()

		self.assertFalse(isLocked)
		logDebug.assert_called_once_with(
			f"Unable to determine lock state via Session Query. "
			f"Lock state value: {WTS_LockState.WTS_SESSIONSTATE_UNKNOWN!r}",
		)
		logError.assert_not_called()

	def test_unknownLockState_outsideWinPE_isTreatedAsUnlockedWithAnError(self):
		with (
			mock.patch.object(
				sessionTracking,
				"_getSessionLockedValue",
				return_value=WTS_LockState.WTS_SESSIONSTATE_UNKNOWN,
			),
			mock.patch.object(sessionTracking.winVersion, "isRunningInWinPE", return_value=False),
			mock.patch.object(sessionTracking.log, "debug") as logDebug,
			mock.patch.object(sessionTracking.log, "error") as logError,
		):
			isLocked = sessionTracking._isWindowsLocked_checkViaSessionQuery()

		self.assertFalse(isLocked)
		logDebug.assert_not_called()
		logError.assert_called_once_with(
			f"Unable to determine lock state via Session Query. "
			f"Lock state value: {WTS_LockState.WTS_SESSIONSTATE_UNKNOWN!r}",
		)
