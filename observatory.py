import os
import os.path as op
import ephem
from numpy import pi
import numpy as np
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import AltAz
from datetime import datetime
import math
import random
from telescope import telescope
from ArScreens import ArScreens
name = 'TIDO'
longitude=93.20
latitude=38.45
elevation=4200
Cloud_dir = op.dirname(op.abspath(__file__)) + "/data/cloud/"
telescope_list = [
                   {'signal': 1, 'caliber': 1, 'field': 3},
                   {'signal': 2, 'caliber': 1, 'field': 3},
                   {'signal': 3, 'caliber': 1, 'field': 3},
                   {'signal': 4, 'caliber': 1, 'field': 3},
                   {'signal': 5, 'caliber': 1, 'field': 3},
                   {'signal': 6, 'caliber': 1, 'field': 3},
                  ]

"记得把时间转换和角度转换写好"

class Observatory:
    def __init__(self, name, Longitude, Latitude, Elevation, telescope_list, Cloud_Cover):

        self.name,self.Longitude,self.Latitude,self.Elevation = name, Longitude, Latitude, Elevation  # 台址信息

        self.Cloud_Cover = Cloud_Cover
        if self.Cloud_Cover is True:
            paramcube = np.array([(0.2, 40, 0, 7600),
                                  (0.2, 5.7, 320, 16000),
                                  ])
            self.cal_cloud = ArScreens(36, 10, 8.4/(36*10), 300., paramcube, 0.99, ranseed=1)
            self.cal_cloud.run(1, verbose=False)
            self.cloud = np.array(np.sum(np.squeeze(self.cal_cloud.screens), 0))[0:360,0:75]

        self.ephem_observatory = ephem.Observer()
        self.ephem_observatory.lat, self.ephem_observatory.lon, self.ephem_observatory.elev = self.Longitude, \
                            self.Latitude, self.Elevation
        self.ephem_moon = ephem.Moon()
        self.ephem_Sun = ephem.Sun()

        self.observation = np.zeros(360*75).reshape(360,75)

        self.telescope_list = telescope_list
        self.telescope_array = list(map(self.create_telescope,telescope_list))  # 根据望远镜参数生成望远镜阵列对象

    def __repr__(self):
        return "{__class__.__name__}({name!r},{Longitude!r},{Latitude!r},{Elevation!r},{_telescope_array!r})"\
            .format(__class__=self.__class__,_telescope_array=",".join(map(repr, self.telescope_list)),**self.__dict__)

    def __str__(self):
        return "{__class__.__name__}({name!r},{Longitude!r},{Latitude!r},{Elevation!r})"\
            .format(__class__=self.__class__,**self.__dict__)

    def __eq__(self, other):
        return self.name == other.name and self.Longitude == other.Longitude and self.Latitude == other.Latitude and \
                self.Elevation == other.Elevation

    def reset(self):
        '''
        将对象所有属性重新设置为初始状态
        :return:
        '''
        pass

    def step(self,time,object_type,moni_object):
        '''
        按照虚拟环境中的时间更新，更新对象中的某些属性
        :return:
        '''
        self.ephem_observatory.date = time

        self._get_ob(object_type, moni_object)
        for telescope in self.telescope_array:
            telescope.step(self.observation)
        if self.Cloud_Cover is True:
            self.cal_cloud.run(1, verbose=False)
            self.cloud = np.array(np.sum(np.squeeze(self.cal_cloud.screens), 0))[0:360, 0:75]

    def _get_ob(self,object_type,moni_object):
        for object_type in object_type:
            for target_index, target in enumerate(moni_object[object_type]):
                az,alt,mag = target.pre_status(observatory=self.ephem_observatory)
                AZ,ALT = math.floor(az*180/pi),math.floor(alt*180/pi)
                if 10 <= ALT < 85:
                    self.observation[AZ][ALT-10] = mag


    def create_telescope(self,dict):
        '''
        生成一个望远镜对象
        :param dict: 望远镜参数
        :return: 望远镜对象
        '''
        telescope_I = telescope(dict['signal'], dict['caliber'], dict['field'], control = dict['control'])
        return telescope_I


    def solar_altitude(self):
        '''
        计算当前台址的太阳高度角
        :param time: 时间，type(astropy.time.Time)
        :return: 太阳高度角，type(astropy.u.deg)
        '''
        # TIDO = Observer(longitude=self.Longitude * u.deg, latitude=self.Latitude* u.deg,
        #                 elevation=self.Elevation * u.m)
        # solar_altitude = TIDO.altaz(time, target=astropy.coordinates.get_sun(time)).alt
        self.ephem_Sun.compute(self.ephem_observatory)
        return float(self.ephem_Sun.alt)

    def is_night(self,time):
        '''
        根据当前太阳高度角判断是否为夜晚
        :param time: 时间，type(ephem.Date)
        :return: bool
        '''
        # time = str(ephem.Date(time))
        # time = Time(datetime.strptime(time, '%Y/%m/%d %H:%M:%S').isoformat(), format='isot')
        if self.solar_altitude() < -6*pi/180 :
            return True
        else:
            return False

    def is_twilight(self,time,type = 1):
        '''
        根据当前太阳高度角判断是否处于晨昏线内
        :param time: 时间，type(ephem.Date)
        :param type: 三种晨昏方式
        :return: bool
        '''
        # time = str(ephem.Date(time))
        # time = Time(datetime.strptime(time, '%Y/%m/%d %H:%M:%S').isoformat(), format='isot')
        if type not in [1,2,3]:
            raise StopIteration("is_twilight type must be 1,2 or 3.")
        if -6*type*pi/180 <= self.solar_altitude() <= 0 *pi/180:
            return True
        else:
            return False

    # def cal_cloud(self):
    #     '''
    #     计算台址当前时间的天区云量
    #     :return: 台址当前时间的天区云量,type(numpy.array)
    #     '''
    #     try :
    #         cloud_dir = op.join(self.Cloud_dir,random.choice(os.listdir(self.Cloud_dir)))
    #         cloud_file = op.join(cloud_dir,os.listdir(cloud_dir)[self.cloud_index])
    #         self.cloud_index += 1
    #         self.cloud_index %= len(cloud_dir)
    #     except:
    #         raise StopIteration("云层文件夹中文件用完")
    #     self.cloud = np.load(cloud_file)[10:85,0:360]
    #     return self.cloud

    def Toazalt(self,ra,dec,time,height):
        '''
        将天球坐标系坐标转换为以当前台址为基点的地平坐标系坐标
        :param ra: 赤经，type(?)
        :param dec: 赤纬，type(?)
        :param time: 时间，type(astropy.time.Time)
        :param height: 高度，
        :return: 高度角，type(?)；方位角，type(?)
        '''
        ra_1 = math.degrees(float(ra))  # 先将弧度转化为角度
        dec_1 = math.degrees(float(dec))
        LAT, LON = float(self.T.lat), float(self.T.lon)
        # 转化将"2022/2/21 00:00:00"转化为2022-02-21T00:00:00.000
        time = str(ephem.Date(time))
        a = datetime.strptime(time, '%Y/%m/%d %H:%M:%S').isoformat()
        obstime = Time(a, format='isot')
        location = EarthLocation.from_geodetic(LAT, LON)
        local_altaz = AltAz(obstime=obstime, location=location)
        icrs = SkyCoord(ra_1 * u.degree, dec_1 * u.degree, frame='icrs')
        altaz = icrs.transform_to(local_altaz)
        az = (altaz.az * u.deg).value
        alt = (altaz.alt * u.deg).value
        return az*pi/180, alt*pi/180

    def cal_Azalt(self,celestical_object,date):
        self.ephem_observatory.date = date
        try:
            celestical_object.ephem_body.compute(self.ephem_observatory.date)
            return celestical_object.ephem_body.az,celestical_object.ephem_body.alt
        except:
            print("Something else went wrong,你可能没有输入观测点的date")

#
# import configparser
# curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
# env_config = configparser.ConfigParser()
# env_config.read(curr_path+"/config/env.ini ", encoding='utf-8')
#
# ob = configparser.ConfigParser()
# ob.read('config/Observatorys.ini', encoding='utf-8')
#
# Observatorys = []
# for observatory in env_config.options("Observatorys"):
#     section = eval(env_config.get("Observatorys", observatory))
#     telescopes, signal = [], 0
#     for tele in eval(ob.get(section, 'telescope')):
#         signal += 1
#         telescopes.append(
#             {'signal': signal,
#              'caliber': eval(ob.get(tele, 'caliber')),
#              'field': eval(ob.get(tele, 'field'))}
#         )
#     name = eval(ob.get(section, 'name'))
#     longitude = eval(ob.get(section, 'longitude'))
#     latitude = eval(ob.get(section, 'latitude'))
#     elevation = eval(ob.get(section, 'elevation'))
#     Cloud_cover = eval(ob.get(section, 'Cloud_cover'))
#     print(name, longitude, latitude, elevation, telescopes, Cloud_cover)
#
#     ob = Observatory(name, longitude, latitude, elevation, telescopes, Cloud_cover)
#     print(ob.telescope_array)
#     Observatorys.append(ob)
