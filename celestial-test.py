from datetime import datetime
from dateutil import tz

from celestial import Celestial

m1 = Celestial(
  name='M1',
  common_name='The Crab Nebula',
  object_type="Supernova Remnant",
  constellation="Taurus",
  distance=6.5,
  ra=[5, 34.5],
  dec=[22, 1]
)
ny_tz = tz.gettz('America/New_York')
date = datetime(2021, 1, 8, 23, 0, 0, tzinfo=ny_tz)
m1_altaz = m1.calc_altaz(date.astimezone(tz=tz.UTC), [42, 21], [-71, 3])
print('Alt: ', m1_altaz['altitude'])
print('Az: ', m1_altaz['azimuth'])