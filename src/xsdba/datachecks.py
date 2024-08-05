"""# noqa: SS01
Data Checks
===========

Utilities designed to check the validity of data inputs.
"""

from __future__ import annotations

from collections.abc import Sequence

import xarray as xr

from .calendar import compare_offsets, parse_offset
from .logging import ValidationError
from .options import datacheck


@datacheck
def check_freq(var: xr.DataArray, freq: str | Sequence[str], strict: bool = True):
    """Raise an error if not series has not the expected temporal frequency or is not monotonically increasing.

    Parameters
    ----------
    var : xr.DataArray
        Input array.
    freq : str or sequence of str
        The expected temporal frequencies, using Pandas frequency terminology ({'Y', 'M', 'D', 'h', 'min', 's', 'ms', 'us'})
        and multiples thereof. To test strictly for 'W', pass '7D' with `strict=True`.
        This ignores the start/end flag and the anchor (ex: 'YS-JUL' will validate against 'Y').
    strict : bool
        Whether multiples of the frequencies are considered invalid or not. With `strict` set to False, a '3h' series
        will not raise an error if freq is set to 'h'.

    Raises
    ------
    ValidationError
        - If the frequency of `var` is not inferrable.
        - If the frequency of `var` does not match the requested `freq`.
    """
    if isinstance(freq, str):
        freq = [freq]
    exp_base = [parse_offset(frq)[1] for frq in freq]
    v_freq = xr.infer_freq(var.time)
    if v_freq is None:
        raise ValidationError(
            "Unable to infer the frequency of the time series. "
            "To mute this, set xsdba's option data_validation='log'."
        )
    v_base = parse_offset(v_freq)[1]
    if v_base not in exp_base or (
        strict and all(compare_offsets(v_freq, "!=", frq) for frq in freq)
    ):
        raise ValidationError(
            f"Frequency of time series not {'strictly' if strict else ''} in {freq}. "
            "To mute this, set xsdba's option data_validation='log'."
        )


def check_daily(var: xr.DataArray):
    """Raise an error if not series has a frequency other that daily, or is not monotonically increasing.

    Notes
    -----
    This does not check for gaps in series.
    """
    return check_freq(var, "D")


@datacheck
def check_common_time(inputs: Sequence[xr.DataArray]):
    """Raise an error if the list of inputs doesn't have a single common frequency.

    Raises
    ------
    ValidationError
        - if the frequency of any input can't be inferred
        - if inputs have different frequencies
        - if inputs have a daily or hourly frequency, but they are not given at the same time of day.

    Parameters
    ----------
    inputs : Sequence of xr.DataArray
        Input arrays.
    """
    # Check all have the same freq
    freqs = [xr.infer_freq(da.time) for da in inputs]
    if None in freqs:
        raise ValidationError(
            "Unable to infer the frequency of the time series. "
            "To mute this, set xsdba's option data_validation='log'."
        )
    if len(set(freqs)) != 1:
        raise ValidationError(
            f"Inputs have different frequencies. Got : {freqs}."
            "To mute this, set xsdba's option data_validation='log'."
        )

    # Check if anchor is the same
    freq = freqs[0]
    base = parse_offset(freq)[1]
    fmt = {"h": ":%M", "D": "%H:%M"}
    if base in fmt:
        outs = {da.indexes["time"][0].strftime(fmt[base]) for da in inputs}
        if len(outs) > 1:
            raise ValidationError(
                f"All inputs have the same frequency ({freq}), but they are not anchored on the same minutes (got {outs}). "
                f"xarray's alignment would silently fail. You can try to fix this with `da.resample('{freq}').mean()`."
                "To mute this, set xsdba's option data_validation='log'."
            )


def is_percentile_dataarray(source: xr.DataArray) -> bool:
    """Evaluate whether a DataArray is a Percentile.

    A percentile dataarray must have climatology_bounds attributes and either a
    quantile or percentiles coordinate, the window is not mandatory.
    """
    return (
        isinstance(source, xr.DataArray)
        and source.attrs.get("climatology_bounds", None) is not None
        and ("quantile" in source.coords or "percentiles" in source.coords)
    )
