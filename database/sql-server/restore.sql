/**
* Author: rgb-24bit
* Date: 2017-12-19
* UpdateDate: 2017-12-20
*
* Des: 还原脚本
*
*/

/* 进入系统库 */
USE master;
GO

/* 还原数据库 */
RESTORE DATABASE company
   FROM DISK = 'd:\company.bak'
   WITH MOVE 'company_data' TO 'c:\data\company_data.mdf',
        MOVE 'company_log'  TO 'c:\data\company_log.ldf';  -- 设置还原路径
GO

/**
* 如果还原失败的原因是未找到相应属性, 请执行
* RESTORE FILELISTONLY FROM DISK='backfile'
* 获取数据文件及日志文件名
*
* 注: c:\data\ 目录必须存在
*
*/

