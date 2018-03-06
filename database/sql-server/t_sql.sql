/*
首先，要认清数据库登录名和数据库用户名之间的关系。数据库登录名和数据库用户名是有差别的，在一个数据库中是一一相对应的关系。
如果把数据库比作一个大厦，那么数据库登录名就是进入大厦的通行证，而用户名则是进入大厦房间的钥匙，
如果每个房间看做是Sql数据库（大厦）的一个数据库，那么每个登录名可以在每一个数据库中创建一个用户，如果没有创建用户，则登录名就只能纯粹的登陆数据库，什么事情都干不了
 */





/* 创建登录名 */
CREATE LOGIN login_name
  WITH PASSWORD = 'password'
  MUST CHANGE;  -- MUST CHANGE 表名用户首次链接时必须修改密码(可选)

/* 创建用户名 */
CREATE USER user_name
   FOR LOGIN login_name;  -- 需要制定登录名

/* 简单方式 */
EXEC SP_ADDLOGIN login_name, password;  -- 逗号
EXEC SP_ADDUSER user_name, login_name;  -- 逗号

/* 创建数据库角色 */
CREATE ROLE role_name;

/* 添加成员 */
ALTER ROLE role_name ADD MEMBER user_name;  -- 2012+

/* 简单方式 */
EXEC SP_ADDROLEMEMBER role_name, user_name;  -- 逗号

/* 删除成员 */
ALTER ROLE role_name DROP MEMBER user_name;

/* 赋予权限 */
GRANT <权限列表>  -- 逗号分隔
   ON <关系或视图名>
   TO <用户或角色列表>
