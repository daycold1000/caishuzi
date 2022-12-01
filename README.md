# 猜数字
注意：功能只适用于NoneBot，并未在NoneBot2中进行测试！

## 简介
这是一个很简单的小游戏，俗称1A2B猜谜。玩家拥有6次机会猜测一个从0~9随机抽取和排列的4位不重复数字，每次猜测都会给出提示直到猜对或次数用尽

## 指令
猜数字
XXXX（X代表数字）

## 部署教程：
1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/daycold1000/caishuzi

2.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'caishuzi'

然后重启 HoshinoBot

## 多余的代码
功能是以我的机器人为主编写的，其中添加了我机器人的功能互通货币和互通道具

一眼看穿：在生成的数字中随机提示一个数字和它所在的位置

暗中调换：在生成的数字中随机替换一个数字并和其他三位数字中的随机一位调换位置



如不需要可删除446行后面的所有内容：

```

@sv.on_fullmatch(['使用道具 一眼看穿'])

......

```


和131行至348行的代码内容：

```

# 创建DB数据

class chouka:

......

"INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",

(gid, uid, msg1),

)

```


还有25、26行代码

```

DB2_PATH = os.path.expanduser('~/.q2bot/chouka.db')

DB_PATH2 = os.path.expanduser('~/.q2bot/shop.db')

```

