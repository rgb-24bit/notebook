/**
* Author: rgb-24bit
* Date: 2017-12-19
* UpdateDate: 2017-12-20
*
* Des: 备份脚本
*
*/

/* 进入系统库 */
USE master;
GO

/* 备份数据库 */
BACKUP DATABASE company
    TO DISK = 'd:\company.bak';
GO

