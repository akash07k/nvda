# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by magnification.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, WINFUNCTYPE, Structure, WinError, c_float, c_int, windll
from ctypes.wintypes import BOOL, LPRECT
from _ctypes import CFuncPtr
from typing import Any

try:
	dll = windll.Magnification
except (AttributeError, OSError):
	dll = None

isAvailable = dll is not None


class MAGCOLOREFFECT(Structure):
	"""
	Describes a color transformation matrix that a magnifier control uses to apply a color effect to magnified screen content.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/magnification/ns-magnification-magcoloreffect
	"""

	_fields_ = (("transform", c_float * 5 * 5),)


PMAGCOLOREFFECT = POINTER(MAGCOLOREFFECT)


def _errCheck[T: tuple[Any]](result: int, func: CFuncPtr, args: T) -> T:
	if result == 0:
		raise WinError()
	return args


if isAvailable:
	MagSetFullscreenColorEffect = WINFUNCTYPE(BOOL, PMAGCOLOREFFECT)(
		("MagSetFullscreenColorEffect", dll),
		((1, "pEffect"),),
	)
	MagSetFullscreenColorEffect.errcheck = _errCheck

	MagGetFullscreenColorEffect = WINFUNCTYPE(BOOL, PMAGCOLOREFFECT)(
		("MagGetFullscreenColorEffect", dll),
		((2, "effect"),),
	)
	MagGetFullscreenColorEffect.errcheck = _errCheck

	MagShowSystemCursor = WINFUNCTYPE(BOOL, BOOL)(
		("MagShowSystemCursor", dll),
		((1, "showCursor"),),
	)
	MagShowSystemCursor.errcheck = _errCheck

	MagInitialize = WINFUNCTYPE(BOOL)(("MagInitialize", dll))
	MagInitialize.errcheck = _errCheck

	MagUninitialize = WINFUNCTYPE(BOOL)(("MagUninitialize", dll))
	MagUninitialize.errcheck = _errCheck

	MagSetFullscreenTransform = WINFUNCTYPE(BOOL, c_float, c_int, c_int)(
		("MagSetFullscreenTransform", dll),
		((1, "magLevel"), (1, "xOffset"), (1, "yOffset")),
	)
	MagSetFullscreenTransform.errcheck = _errCheck

	MagSetInputTransform = WINFUNCTYPE(BOOL, BOOL, LPRECT, LPRECT)(
		("MagSetInputTransform", dll),
		((1, "fEnabled"), (1, "pRectSource"), (1, "pRectDest")),
	)
	MagSetInputTransform.errcheck = _errCheck
else:

	def _unavailable(*args: Any) -> None:
		raise OSError("The Magnification API is not available")

	MagSetFullscreenColorEffect = _unavailable
	MagGetFullscreenColorEffect = _unavailable
	MagShowSystemCursor = _unavailable
	MagInitialize = _unavailable
	MagUninitialize = _unavailable
	MagSetFullscreenTransform = _unavailable
	MagSetInputTransform = _unavailable
