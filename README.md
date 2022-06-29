# taptap-spider
用于爬取taptap平台内游戏的相关数据，为数据分析项目提供数据支持。

一次爬取的数据量在500MB左右，耗时四天。


### 结构：
1. ProjSetting.py 定义了项目用到的url和请求头
2. run.py 定义了项目的日志规格和存储位置、利用twist异步管理框架分步执行爬虫进程
3. Scheduler.py 定义了项目的定时器，用于在每周日凌晨0点执行爬虫任务，并在爬虫执行完毕后唤醒数据分析后端进行数据处理和更新。
4. taptap/spiders/*.py 定义了用到的爬虫。
5. taptap/pipelines.py 定义了爬取到的items的处理逻辑。在爬取完毕后执行评论的清洗和分词工作。 

### 待处理工作：
1. 日志记录和定时器（已完成）
2. 执行完毕后调用数据分析后端执行分析（未完成）
