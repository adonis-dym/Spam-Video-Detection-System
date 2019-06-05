
## SQL结构
| | |
|---|---|
|ip| 1.1.1.1
|user| bilibili
|password| *********
|database| bilibili
|phpmyadmin| http://1.1.1.1/phpMyAdmin/
|table| info

### 数据库bilibili结构
- audience_statistics 表 ： 每隔10秒钟在线人数等信息的统计
- info_random 表：aid 在30000000 - 40000000直接随机选取100000个有效的视频进行爬取
- info 表：从头开始爬的大概1000万条数据

**字段说明**

| | | |
|---|---|---|
|aid        |视频编号|2
|tid        |分类编号|12
|tname      |分类名称|""
|pic        |封面图片|"http://static.hdslb.com/images/transparent.gif"
|title      |标题    |"字幕君交流场所"
|pubdate    |发布时间|1252458549
|description|描述    |"www"
|duration   |持续时间|2055
|owner_mid  |发布者id|2
|owner_name |发布者名称|"碧诗"
|view_num   |播放量  |743152
|danmaku    |弹幕数  |39366
|reply      |评论数  |36940
|favorite   |收藏数  |21334
|coin       |硬币数  |7919
|share_num  |分享数  |3785
|like_num   |喜欢数  |19283
|dislike    |不喜欢数|0


建表代码：

    """
    CREATE TABLE info (
        aid        int not null,
        tid        int,
        tname      text,
        pic        text,
        title      text,
        pubdate    int,
        description text,
        duration   int,
        owner_mid  int,
        owner_name text,
        view_num   int,
        danmaku    int,
        reply      int,
        favorite   int,
        coin       int,
        share_num  int,
        like_num   int,
        dislike    int,
        primary key (aid)
        )
    """

    """
    CREATE TABLE info_random (
        id         int NOT NULL AUTO_INCREMENT,
        aid        int NOT NULL distinct,
        tid        int,
        tname      text,
        pic        text,
        title      text,
        pubdate    int,
        description text,
        duration   int,
        owner_mid  int,
        owner_name text,
        view_num   int,
        danmaku    int,
        reply      int,
        favorite   int,
        coin       int,
        share_num  int,
        like_num   int,
        dislike    int,
        primary key (id)
        )
    """

## 已爬取aid区间
- 30000000 - 40000000直接随机选取100000个有效的视频进行爬取



    """
    CREATE TABLE audience_statistics (
        id         int NOT NULL AUTO_INCREMENT,
        time       timestamp NOT NULL default CURRENT_TIMESTAMP,
        all_count  int,
        web_online int,
        play_online int,
        primary key (id)
        )
    """
| | | |
|---|---|---|
|all_count        |最新投稿|41169
|web_online        |在线人数|2640059
|play_online      | |3431483


