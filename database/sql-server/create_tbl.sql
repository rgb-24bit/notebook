/**
 * Author: rgb-24bit
 * Date: 2017-12-14
 * UpdateDate: 2017-12-19
 *
 * Des: 建表脚本
 *
 */

/* 进入company数据库 */
USE company;
GO


/* 创建员工表 */
PRINT 'Create Table employee';
IF OBJECT_ID('employee') IS NOT NULL
   DROP TABLE employee;  -- 如果员工表存在便删除
GO

CREATE TABLE employee (
    PRIMARY KEY (SSN),
    FNAME    NVARCHAR(20)  NOT NULL,
    MINIT    NVARCHAR(1)   NOT NULL,
             CONSTRAINT CK_EMPLOYEE_MINIT
             CHECK(MINIT LIKE '[A-Z|a-z]'),  -- MINIT 只能是单个字母
    LNAME    NVARCHAR(20)  NOT NULL,
    SSN      DECIMAL(9, 0) NOT NULL,
    BDATE    DATE          NOT NULL,
    ADDRESS  NVARCHAR(50)  NOT NULL,
    SEX      NVARCHAR(1)   NOT NULL,
             CONSTRAINT CK_EMPLOYEE_SEX
             CHECK (SEX IN ('F', 'M')),  -- SEX 只能是 F or M
    SALARY   INT           NOT NULL,
             CONSTRAINT CK_EMPLOYEE_SALARY
             CHECK (SALARY > 0),  -- SALARY 应该大于 0
    SUPERSSN DECIMAL(9, 0),
    DNO      TINYINT       NOT NULL
);
GO

/* 创建部门表 */
PRINT 'Create table department';
IF OBJECT_ID('department') IS NOT NULL
   DROP TABLE department;
GO

CREATE TABLE department (
    PRIMARY KEY (DNUMBER),
    DNAME           NVARCHAR(20)  NOT NULL,
    DNUMBER         TINYINT       NOT NULL,
    MGRSSN          DECIMAL(9, 0) NOT NULL,
    MGRSTARTDATE    DATE          NOT NULL
);
GO

/* 创建部门地址表 */
PRINT 'Create table dept_location';
IF OBJECT_ID('dept_location') IS NOT NULL
   DROP TABLE dept_location;
GO

CREATE TABLE dept_location (
    PRIMARY KEY (DNUMBER, DLOCATION),
    DNUMBER     TINYINT      NOT NULL,
    DLOCATION   NVARCHAR(20) NOT NULL,
);
GO

/* 创建工作表 */
PRINT 'Create table works_on';
IF OBJECT_ID('works_on') IS NOT NULL
   DROP TABLE works_on;
GO

CREATE TABLE works_on (
    PRIMARY KEY (ESSN, PNO),
    ESSN    DECIMAL(9, 0) NOT NULL,
    PNO     INT           NOT NULL,
    HOURS   DECIMAL(3, 1),
);
GO

/* 创建项目表 */
PRINT 'Create table project';
IF OBJECT_ID('project') IS NOT NULL
   DROP TABLE project;
GO

CREATE TABLE project (
    PRIMARY KEY (PNUMBER),
    PNAME     NVARCHAR(20) NOT NULL,
    PNUMBER   INT          NOT NULL,
    PLOCATION NVARCHAR(20) NOT NULL,
    DNUM      TINYINT      NOT NULL
)
GO

/* 创建家属表 */
PRINT 'Create table dependent';
IF OBJECT_ID('dependent') IS NOT NULL
   DROP TABLE dependent;
GO

CREATE TABLE dependent (
    PRIMARY KEY (ESSN, DEPENDENT_NAME),
    ESSN            DECIMAL(9, 0)  NOT NULL,
    DEPENDENT_NAME  NVARCHAR(20)   NOT NULL,
    SEX             NVARCHAR(1)    NOT NULL,
                    CONSTRAINT CK_DEPENDENT_SEX
                    CHECK (SEX IN ('F', 'M')),  -- SEX 只能是 F or M
    BDATE           DATE           NOT NULL,
    RELATIONSHIP    NVARCHAR(20)   NOT NULL,
);
GO


/* 添加外键约束 */
PRINT 'Add Refential Integrity Constraint';
GO

ALTER TABLE employee
        ADD CONSTRAINT FK_EMPLOYEE_EMPLOYEE
    FOREIGN KEY (SUPERSSN) REFERENCES employee(SSN);  -- employee.SUPERSSN --> employee.SSN

ALTER TABLE employee
        ADD CONSTRAINT FK_EMPLOYEE_DEPARTMENT
    FOREIGN KEY (DNO) REFERENCES department(DNUMBER);  -- employee.DNO --> department.DNUMBER

ALTER TABLE department
        ADD CONSTRAINT FK_DEPARTMENT_EMPLOYEE
    FOREIGN KEY (MGRSSN) REFERENCES employee(SSN);  -- department.MGRSSN --> employee.SSN

ALTER TABLE dept_location
        ADD CONSTRAINT FK_DEPT_DEPARTMENT
    FOREIGN KEY (DNUMBER) REFERENCES department(DNUMBER);  -- dept_location.DNUMBER --> department.DNUMBER

ALTER TABLE project
        ADD CONSTRAINT FK_PROJECT_DEPARTMENT
    FOREIGN KEY (DNUM) REFERENCES department(DNUMBER);  -- project.DNUM --> department.DNUMBER

ALTER TABLE works_on
       ADD CONSTRAINT FK_WORKS_EMPLOYEE
   FOREIGN KEY (ESSN) REFERENCES employee(SSN);  -- works_on.ESSN --> employee.SSN

ALTER TABLE works_on
        ADD CONSTRAINT FK_WORKS_PROJECT
    FOREIGN KEY (PNO) REFERENCES project(PNUMBER); -- works_on.PNO --> project.PNUMBER

ALTER TABLE dependent
        ADD CONSTRAINT FK_DEPENDENT_EMPLOYEE
    FOREIGN KEY (ESSN) REFERENCES employee(SSN);  -- dependent.ESSN --> employee.SSN
GO

/* 建表完成 */
PRINT 'Create table Complete';
GO

