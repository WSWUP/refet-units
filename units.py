import math


DEFAULT_UNITS = [
    'c', 'celsius',
    'mj m-2 d-1', 'mj m-2 day-1',
    'mj m-2 h-1', 'mj m-2 hr-1', 'mj m-2 hour-1',
    'kpa',
    'm s-1', 'm/s',
    'm', 'meter', 'meters',
    'deg', 'degree', 'degrees',
    'mm/d','mm d-1',
]
RS_HOURLY_UNITS = [
    'w m-2 h-1', 'w m-2 hr-1', 'w m-2 hour-1', 'w/m2/hr', 'w/m2/hour'
]
RS_DAILY_UNITS = ['w m-2 d-1', 'w m-2 day-1', 'w/m2/d', 'w/m2/day']
SUPPORTED_UNITS = [
    'k', 'kelvin',
    'f', 'fahrenheit',
    'pa', 'mbar', 'atm',
    'torr', 'mmhg',
    'langleys',
    'kw/m2', 'kw m-2','kw/m2','kw/m2',
    'w m-2', 'w/m2',
    'mph', 'kmd','kmh',
    'ft', 'feet',
    'rad', 'radian', 'radians',
    'm/d', 'in/d','ft/d',

]
SUPPORTED_UNITS.extend(RS_HOURLY_UNITS)
SUPPORTED_UNITS.extend(RS_DAILY_UNITS)


def convert(values, variable, unit, timestep=None):
    """Unit conversion function

    Args:
        values: ndarray
        variable: str
        unit: str
        timestep: str, optional
            Must be set when converting Rs W/m2 values.
            Choices are "daily" or "hourly".

    Returns:
        ndarray

    """
    if unit == '':
        return values
    elif unit.lower() in DEFAULT_UNITS:
        return values
    elif unit.lower() not in SUPPORTED_UNITS:
        raise ValueError(f'unsupported unit conversion for {variable} {unit}')

    # Convert input values to expected units
    # TODO: Split these into separate functions
    if variable in ['tmean', 'tmin', 'tmax', 'tdew']:
        if unit.lower() in ['f', 'fahrenheit']:
            values -= 32
            values *= (5.0 / 9)
        elif unit.lower() in ['k', 'kelvin']:
            values -= 273.15
    elif variable in ['precip', 'prec', 'prcp','precipitation']:
        if unit.lower() in ['m/d']:
            values *= 1000
        if unit.lower() in ['in/d']:
            values *= 25.4
        if unit.lower() in ['ft/d']:
            values *= 304.8
    elif variable == 'ea':
        if unit.lower() in ['pa']:
            values /= 1000.0
        if unit.lower() in ['mbar']:
            values /= 0.1
        if unit.lower() in ['atm']:
            values /= 0.00986923
        if unit.lower() in ['torr']:
            values /= 7.50062
        if unit.lower() in ['mmhg']:
            values /= 7.50062
    elif variable == 'rs':
        if unit.lower() in ['langleys']:
            values *= 0.041868
        elif unit.lower() in ['w m-2', 'w/m2']:
            if timestep.lower() == 'daily':
                values *= 0.0864
            elif timestep.lower() == 'hourly':
                values *= 0.0036
            else:
                raise ValueError(f'unsupported rs timestep parameter: {timestep}')
        elif unit.lower() in ['kw/m2', 'kw m-2','kw/m2','kw/m2']:
            if timestep.lower() == 'daily':
                values *= 86.4
            elif timestep.lower() == 'hourly':
                values *= 3.6
            else:
                raise ValueError(f'unsupported rs timestep parameter: {timestep}')
        elif unit.lower() in RS_DAILY_UNITS:
            values *= 0.0864
        elif unit.lower() in RS_HOURLY_UNITS:
            values *= 0.0036
    elif variable == 'uz':
        if unit.lower() in ['mph']:
            values *= 0.44704
        elif unit.lower() in ['kmd']:
            values *= 1000.0 / 86400.0
        elif unit.lower() in ['kmh']:
            values *= 1000.0 / 3600.0
    elif variable in ['zw', 'elev']:
        if unit.lower() in ['ft', 'feet']:
            values *= 0.3048
    elif variable in ['lat', 'lon']:
        if unit.lower() in ['rad', 'radian', 'radians']:
            # This is a little backwards but convert to degrees so that
            # it can be converted to radians below.  This is done so
            # that not setting the value will default to degrees.
            values *= (180.0 / math.pi)

    return values


def _deg2rad(deg):
    """Convert degrees to radians"""
    return deg * math.pi / 180.0


def _rad2deg(rad):
    """Convert radians to degrees"""
    return rad * 180.0 / math.pi


def _c2f(c):
    """Convert Celsius to Fahrenheit"""
    return c * (9.0 / 5) + 32


def _f2c(f):
    """Convert Fahrenheit to Celsius"""
    return (f - 32) * (5.0 / 9)
