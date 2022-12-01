import asyncio
import base64
import os
import random
from re import T, match
import sqlite3
from datetime import datetime, timedelta
from io import SEEK_CUR, BytesIO
from PIL import Image
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import copy
import json
import math
import pytz
import nonebot
from nonebot import on_command, on_request
from hoshino import sucmd
from nonebot import get_bot
from hoshino.typing import NoticeSession

sv = Service('q2猜数字', enable_on_default=True)
DB_PATH = os.path.expanduser('~/.q2bot/caishuzi.db')
DB2_PATH = os.path.expanduser('~/.q2bot/chouka.db')
DB_PATH2 = os.path.expanduser('~/.q2bot/shop.db')

# 创建DB数据
class csz:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_shuzi()
        self._create_cishu()
        

    def _connect(self):
        return sqlite3.connect(DB_PATH)


#生成数字存放
    def _create_shuzi(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SHUZI
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           SHUZI           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_shuzi(self, gid, uid, shuzi):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHUZI (GID, UID, SHUZI) VALUES (?, ?, ?)",
                (gid, uid, shuzi,),
            )

    def _get_shuzi(self, gid, uid):
        try:
            r = self._connect().execute("SELECT SHUZI FROM SHUZI WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    def _add_shuzi(self, gid, uid, num):
        num1 = self._get_shuzi(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHUZI (GID, UID, SHUZI) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )

    def _reduce_shuzi(self, gid, uid, num):
        msg1 = self._get_shuzi(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHUZI (GID, UID, SHUZI) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )

#玩家猜对次数
    def _create_cishu(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CISHU
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           CISHU           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_cishu(self, gid, uid, cishu):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CISHU (GID, UID, CISHU) VALUES (?, ?, ?)",
                (gid, uid, cishu,),
            )

    def _get_cishu(self, gid, uid):
        try:
            r = self._connect().execute("SELECT CISHU FROM CISHU WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    def _add_cishu(self, gid, uid, num):
        num1 = self._get_cishu(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CISHU (GID, UID, CISHU) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )

    def _reduce_cishu(self, gid, uid, num):
        msg1 = self._get_cishu(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CISHU (GID, UID, CISHU) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )


# 创建DB数据
class chouka:
    def __init__(self):
        os.makedirs(os.path.dirname(DB2_PATH), exist_ok=True)
        self._create_shitou()
        

    def _connect(self):
        return sqlite3.connect(DB2_PATH)

#母猪石数量
    def _create_shitou(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SHITOU
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           SHITOU           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_shitou(self, gid, uid, shitou):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, shitou,),
            )

    def _get_shitou(self, gid, uid):
        try:
            r = self._connect().execute("SELECT SHITOU FROM SHITOU WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    def _add_shitou(self, gid, uid, num):
        num1 = self._get_shitou(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )

    def _reduce_shitou(self, gid, uid, num):
        msg1 = self._get_shitou(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )



# 创建DB数据
class shangdian:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH2), exist_ok=True)
        self._create_daoju()
        

    def _connect(self):
        return sqlite3.connect(DB_PATH2)
#道具数量
    def _create_daoju(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUI
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUI           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUII
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUII           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUIII
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUIII           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUIV
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUIV           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_daoju1(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju2(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju3(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju4(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )

    def _get_daoju1(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUI FROM DAOJUI WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju2(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUII FROM DAOJUII WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju3(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUIII FROM DAOJUIII WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju4(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUIV FROM DAOJUIV WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    def _add_daoju1(self, gid, uid, num):
        num1 = self._get_daoju1(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju2(self, gid, uid, num):
        num1 = self._get_daoju2(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju3(self, gid, uid, num):
        num1 = self._get_daoju3(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju4(self, gid, uid, num):
        num1 = self._get_daoju4(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )

    def _reduce_daoju1(self, gid, uid, num):
        msg1 = self._get_daoju1(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju2(self, gid, uid, num):
        msg1 = self._get_daoju2(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju3(self, gid, uid, num):
        msg1 = self._get_daoju3(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju4(self, gid, uid, num):
        msg1 = self._get_daoju4(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )

@sv.on_fullmatch(['猜数字'])
async def chudao1(bot, ev: CQEvent):
    gid = ev.group_id
    q2csz = csz()
    if q2csz._get_shuzi(gid,6) == 1:
        await bot.finish(ev,'猜数字正在进行中~')
    sz1 = random.randint(0,9)
    q2csz._set_shuzi(gid,1,sz1)

    sz2 = random.randint(0,9)
    while sz2 == sz1:
        sz2 = random.randint(0,9)
    q2csz._set_shuzi(gid,2,sz2)

    sz3 = random.randint(0,9)
    while sz3 == sz1 or sz3 == sz2:
        sz3 = random.randint(0,9)
    q2csz._set_shuzi(gid,3,sz3)

    sz4 = random.randint(0,9)
    while sz4 == sz1 or sz4 == sz2 or sz4 == sz3:
        sz4 = random.randint(0,9)
    q2csz._set_shuzi(gid,4,sz4)

    q2csz._set_shuzi(gid,5,6) #6次机会
    q2csz._set_shuzi(gid,6,1) #本群进入猜数字状态，发数字进入有效状态
    q2csz._set_shuzi(gid,7,1) #1次提示
    q2csz._set_shuzi(gid,8,1) #1次捣乱机会

    await bot.send(ev,'我生成了4个不同的数字，快来猜猜吧！(直接发数字）')


@sv.on_rex(r'^(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)$')
async def baodao1(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    q2csz = csz()
    ck = chouka()
    if q2csz._get_shuzi(gid,6) == 0:
        return
    match = (ev['match'])
    num1 = int(match.group(1))
    num2 = int(match.group(2))
    num3 = int(match.group(3))
    num4 = int(match.group(4))
    if num1 == num2 or num1 == num3 or num1 == num4 or num2 == num3 or num2 == num4 or num3 == num4:
        await bot.finish(ev,'是不一样的数字哦！')
    a = 0
    b = 0
    if q2csz._get_shuzi(gid,1) == num1:
        a +=1
    elif q2csz._get_shuzi(gid,1) ==num2 or q2csz._get_shuzi(gid,1) ==num3 or q2csz._get_shuzi(gid,1) ==num4:
        b +=1
    
    if q2csz._get_shuzi(gid,2) == num2:
        a +=1
    elif q2csz._get_shuzi(gid,2) ==num1 or q2csz._get_shuzi(gid,2) ==num3 or q2csz._get_shuzi(gid,2) ==num4:
        b +=1
    
    if q2csz._get_shuzi(gid,3) == num3:
        a +=1
    elif q2csz._get_shuzi(gid,3) ==num2 or q2csz._get_shuzi(gid,3) ==num1 or q2csz._get_shuzi(gid,3) ==num4:
        b +=1
    
    if q2csz._get_shuzi(gid,4) == num4:
        a +=1
    elif q2csz._get_shuzi(gid,4) ==num2 or q2csz._get_shuzi(gid,4) ==num3 or q2csz._get_shuzi(gid,4) ==num1:
        b +=1
    
    if a ==4:
        q2csz._add_cishu(gid,uid,1)
        cishu = q2csz._get_cishu(gid,uid)
        q2csz._set_shuzi(gid,6,0)
        shitou = random.randint(0,100000)
        suipian = random.randint(0,10)
        ck._add_shitou(0,uid,shitou)
        await bot.finish(ev,f'恭喜你，猜对了！\n数字是：{num1}{num2}{num3}{num4}\n喵喵石头x{shitou} 精元碎片x{suipian}\n一共猜对了{cishu}次。')

    q2csz._reduce_shuzi(gid,5,1)
    jihui = q2csz._get_shuzi(gid,5)

    if jihui ==0:
        num1 = q2csz._get_shuzi(gid,1)
        num2 = q2csz._get_shuzi(gid,2)
        num3 = q2csz._get_shuzi(gid,3)
        num4 = q2csz._get_shuzi(gid,4)
        msg = f'机会用完了，正确答案是：{num1}{num2}{num3}{num4}'
        q2csz._set_shuzi(gid,6,0)
        await bot.finish(ev,msg,at_sender=True)

    msg = f'''不对哦！你猜的数字是{num1}{num2}{num3}{num4}
其中{a}个数字存在且位置正确
其中{b}个数字存在且位置不正确
还有{jihui}次机会'''
    await bot.finish(ev,msg,at_sender=True)

@sv.on_fullmatch(['使用道具 一眼看穿'])
async def daoju1(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    q2csz = csz()
    shop = shangdian()
    if q2csz._get_shuzi(gid,6) !=1:
        await bot.finish(ev,'这个群不在猜数字')
    if q2csz._get_shuzi(gid,7) ==1:
        if shop._get_daoju1(0,uid) !=0:
            if q2csz._get_shuzi(gid,5) <=2:
                num = random.randint(1,4)
                num1 = q2csz._get_shuzi(gid,num)
                q2csz._set_shuzi(gid,7,0)
                shop._reduce_daoju1(0,uid,1)
                await bot.finish(ev,f'第{num}位数字是{num1}')
            else:
                await bot.finish(ev,'还有足够的机会呢，多猜猜！')
        else:
            await bot.finish(ev,'你没有 一眼看穿',at_sender=True)
    else:
        await bot.finish(ev,'本群没有提示机会了')

@sv.on_fullmatch(['使用道具 暗中调换'])
async def daoju2(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    q2csz = csz()
    shop = shangdian()
    if q2csz._get_shuzi(gid,6) !=1:
        await bot.finish(ev,'这个群不在猜数字')
    if q2csz._get_shuzi(gid,8) ==1:
        if shop._get_daoju2(0,uid) !=0:
            if q2csz._get_shuzi(gid,5) <=5:
                xunhuan = 1
                while xunhuan !=0:
                    num = random.randint(1,4)
                    num1 = random.randint(0,9)
                    inum1 = q2csz._get_shuzi(gid,1)
                    inum2 = q2csz._get_shuzi(gid,2)
                    inum3 = q2csz._get_shuzi(gid,3)
                    inum4 = q2csz._get_shuzi(gid,4)
                    if num1 == inum1 or num1 == inum2 or num1 == inum3 or num1 == inum4:
                        xunhuan = 1
                    else:
                        inum = q2csz._get_shuzi(gid,num) #替换前看看是什么数字
                        q2csz._set_shuzi(gid,num,num1) #替换数字
                        xunhuan2 = 1
                        while xunhuan2 !=0: #替换位置的循环
                            num2 = random.randint(1,4)
                            if num == num2: #如果随机数和被替换的数字的位置一样则继续
                                xunhuan2 = 1
                            else:
                                shuzi1 = q2csz._get_shuzi(gid,num) #获取被替换数字的数字
                                shuzi2 = q2csz._get_shuzi(gid,num2) #获取未被替换位置数字的数字
                                q2csz._set_shuzi(gid,num2,shuzi1)
                                q2csz._set_shuzi(gid,num,shuzi2) #交换位置
                                xunhuan2 = 0
                        xunhuan = 0

                q2csz._set_shuzi(gid,8,0)
                shop._reduce_daoju2(0,uid,1)
                await bot.finish(ev,f'捣乱成功，数字{inum}被替换成{num1}并与存在的其中一个数字调换了位置')
            else:
                await bot.finish(ev,'还有足够的机会呢，让ta多猜猜！')
        else:
            await bot.finish(ev,'你没有 暗中调换',at_sender=True)
    else:
        await bot.finish(ev,'本群没有捣乱机会了')