from math import sin, cos, asin, acos, radians, degrees, floor, pow, pi

class Celestial:

  def __init__(self, name, object_type, distance, constellation, ra, dec, common_name=''):
    self.name = name
    self.common_name = common_name
    self.object_type = object_type
    self.distance = distance # Kilo-lightyears
    self.constellation = constellation
    self.ra = ra # [hours, minutes]
    self.dec = dec # [degrees, minutes]
    self.ra_real = self.__ra2real(ra[0], ra[1])
    self.dec_real = self.__dm2real(dec[0], dec[1])

  # Calcualtes number of days since J2000 from target date
  def __days_since_J2000(self, date):
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second

    if month == 1 or month == 2:
      year  = year - 1
      month = month + 12

    a = floor(year / 100)
    b = 2 - a + floor(a / 4)
    c = floor(365.25 * year)
    d = floor(30.6001 * (month + 1))
    return b + c + d - 730550.5 + day + (hour + minute / 60.0 + second / 3600.0) / 24.0

  # Returns local siderial time
  def __mean_siderial_time(self, date, lon):
    julian_centuries_since_j2000 = self.__days_since_J2000(date) / 36525.0
    mean_siderial_time = (280.46061837 + 360.98564736629
      * self.__days_since_J2000(date) + 0.000387933
      * pow(julian_centuries_since_j2000, 2)
      - pow(julian_centuries_since_j2000, 3) / 38710000 + lon
    )

    if (mean_siderial_time < 0):
      while mean_siderial_time < 0 :
        mean_siderial_time += 360
    elif (mean_siderial_time > 360):
      while mean_siderial_time > 360:
        mean_siderial_time -= 360

    return mean_siderial_time

  # Returns the horizon angle
  def __horizon_angle(self, date, lon):
    horizon_angle = self.__mean_siderial_time(date, lon) - self.ra_real
    if horizon_angle < 0:
      horizon_angle += 360
    return horizon_angle

  # Parameters in degrees
  # Returns altitude in degrees
  def __altitude(self, lat, ha):
    dec = radians(self.dec_real)
    lat = radians(lat)
    ha = radians(ha)
    sin_alt = sin(dec) * sin(lat) + cos(dec) * cos(lat) * cos(ha)
    return degrees(asin(sin_alt))

  # Parameters in degrees
  # Returns azimuth in degrees
  def __azimuth(self, lat, alt, ha):
    dec = radians(self.dec_real)
    lat = radians(lat)
    ha = radians(ha)
    alt = radians(alt)
    cos_az = (sin(dec) - sin(alt) * sin(lat)) / (cos(alt) * cos(lat))
    az = degrees(acos(cos_az))
    return 360 - az if sin(ha) > 0 else az

  # Converts right ascension from hours minutes to a real number
  def __ra2real(self, hrs, mins):
    return 15 * (hrs + mins / 60)

  # Converts right ascension from hours minutes to a real number
  def __dm2real(self, deg, min):
    return deg - min / 60 if deg < 0 else deg + min / 60

  # Parameters:
  # date - datetime object in UTC
  # lat - latitude in degrees minutes as an array e.g. [42, 21]
  #       Positive for East Longitude, Negative for West
  # lon - longitude in degrees minutes as an array e.g. [-71, 3]
  # Returns dict with keys "altitude" and "azimuth"
  def calc_altaz(self, date, lat_dm, lon_dm):
    lat = self.__dm2real(lat_dm[0], lat_dm[1])
    lon = self.__dm2real(lon_dm[0], lon_dm[1])
    ha = self.__horizon_angle(date, lon)
    alt = self.__altitude(lat, ha)
    return {
      'altitude': alt,
      'azimuth': self.__azimuth(lat, alt, ha)
    }
