import pymysql
#打开数据库连接
user = input("mysql username:")
passwd = input("mysql passwd:")
conn = pymysql.connect(user=user, passwd=passwd, db="MinerLog")
cursor = conn.cursor()

sql = 'CREATE TABLE IF NOT EXISTS `powerlog`( ' \
      '`id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY UNIQUE NOT NULL, ' \
      '`date` DATE, ' \
      '`name` VARCHAR(10) NOT NULL, ' \
      '`power` FLOAT);'
cursor.execute(sql)

cursor.close()#先关闭游标
conn.close()#再关闭数据库连接
print('create table success')
