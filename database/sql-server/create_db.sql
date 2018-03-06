/**
 * Author: rgb_24bit
 * Date: 2017-12-14
 * UpdateDate: 2017-12-19
 *
 * Des: 建库脚本
 *
 */

/* 阻止在结果集中返回显示受T-SQL语句或则usp影响的行计数信息 */
SET NOCOUNT ON;
GO

/* 如果数据库以存在便删除它 */
PRINT 'Create database company';
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'company')
   DROP DATABASE company;
GO

/* 创建数据库 */
CREATE DATABASE company
    ON  -- 指定数据库数据文件路径
     (
       name = company_data,
       filename = 'c:\data\company_data.mdf'
     )
   LOG ON  -- 指定数据库日志文件路径
     (
       name = company_log,
       filename = 'c:\data\company_log.ldf'
     );
GO

/* 如果执行错误便退出sqlcmd */
:On Error exit

/* 执行创建数据表脚本 */
:r c:\data\create_tbl.sql

