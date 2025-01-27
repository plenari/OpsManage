#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
from asset.models import Business_Tree_Assets       

class DataBase_Server_Config(models.Model):
    env_type = (
                ('alpha',u'开发环境'),
                ('beta',u'测试环境'),
                ('ga',u'生产环境'),
                )
    mode = (
            ('single',u'单例'),
            ('ms',u'主从'),
            ('pxc',u'pxc'),
            ('master',u'主库'),
            ) 
    rw_type = (
                ('read',u'只读'),
                ('r/w',u'读写'),
                ('write',u'可写'),
                )  
    dataMap = {
               "env":{
                    'alpha':'开发环境',
                    'beta':'测试环境',
                    'ga':'生产环境',                      
                },
               'mode':{
                    'single':'单例',
                    'ms':'主从',
                    'pxc':'pxc',   
                    'master':'主库',                    
                },
               "rw":{
                    'read':'只读',
                    'r/w':'读写',
                    'write':'可写',                     
                }
               }  
    db_env = models.CharField(choices=env_type,max_length=10,verbose_name='环境类型',default=None)
    db_type = models.CharField(max_length=10,verbose_name='数据库类型',blank=True,null=True)
#     db_name = models.CharField(max_length=100,verbose_name='数据库名',blank=True,null=True)
    db_assets = models.ForeignKey('asset.Assets',related_name='database_total', on_delete=models.CASCADE,verbose_name='assets_id')
    db_business = models.IntegerField(verbose_name='业务关联')
    db_mode = models.CharField(max_length=10,choices=mode,verbose_name='架构类型',default='single')
    db_user = models.CharField(max_length=100,verbose_name='用户',blank=True,null=True)
    db_passwd = models.CharField(max_length=100,verbose_name='密码',blank=True,null=True)
    db_port = models.IntegerField(verbose_name='端口')
    db_version =  models.CharField(max_length=100,verbose_name='数据库版本',blank=True,null=True)
    db_mark =  models.CharField(max_length=100,verbose_name='标识',blank=True,null=True)
    db_rw =  models.CharField(choices=rw_type,max_length=20,verbose_name='读写类型',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_database_server_config'
        default_permissions = ()
        permissions = (
            ("database_read_database_server_config", "读取数据库信息表权限"),
            ("database_change_database_server_config", "更改数据库信息表权限"),
            ("database_add_database_server_config", "添加数据库信息表权限"),
            ("database_delete_database_server_config", "删除数据库信息表权限"),     
            ("database_query_database_server_config", "数据库查询查询权限"), 
			("databases_dml_database_server_config", "数据库执行DML语句权限"), 
            ("database_binlog_database_server_config", "数据库Binglog解析权限"),        
            ("database_schema_database_server_config", "数据库表结构查询权限"),
            ("database_optimize_database_server_config", "数据库SQL优化建议权限"),
        )
        unique_together = (("db_port", "db_assets","db_env"))
        verbose_name = '数据库管理'  
        verbose_name_plural = '数据库信息表'

    def business_paths(self):
        try:
            business = Business_Tree_Assets.objects.get(id=self.db_business)
            return business.business_env() + '/' +business.node_path()
        except:
            return "未知"   
    
    def to_tree(self):
        try:
            db_ip = self.db_assets.server_assets.ip
        except:
            db_ip = '未知'
        json_format = {
            "id":"db_server_"+ str(self.id),
            "db_server": self.id,
            "text": "{mark}({ip}:{port})".format(mark=self.db_mark,ip=db_ip,port=str(self.db_port)),
            "ip":db_ip, 
            "user_id":0,
            "last_node": 1,
            "icon":"fa fa-minus-square-o",          
        }
        return  json_format         
        
    def to_json(self):
        try:
            db_ip = self.db_assets.server_assets.ip
        except:
            db_ip = '未知'
        json_format = {
            "id":self.id,
            "db_env":self.dataMap["env"].get(self.db_env),
            "db_type":self.db_type,
            "db_version":self.db_version,
            "db_assets_id":self.db_assets.id,
            "ip":db_ip,           
            "db_business":self.db_business,
            "db_mode":self.dataMap["mode"].get(self.db_mode),
            "db_business_paths":self.business_paths(),
            "db_port":self.db_port,
            "db_user":self.db_user,
            "db_mark":self.db_mark,
            "db_rw":self.dataMap["rw"].get(self.db_rw),
        }
        return  json_format             

    def to_connect(self):
        json_format = {
            "id":self.id,          
            "db_name":'',
            "ip":self.db_assets.server_assets.ip ,
            "db_port":self.db_port,
            "db_user":self.db_user,
            "db_passwd":self.db_passwd,  
            "db_rw":self.db_rw,          
        }
        return  json_format

class Database_Detail(models.Model):
    db_server = models.ForeignKey('DataBase_Server_Config',related_name='databases', on_delete=models.CASCADE,verbose_name='db_server_id')
    db_name = models.CharField(max_length=50,verbose_name='数据库名字')    
    db_size = models.IntegerField(verbose_name='数据库大小',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_database_detail'
        default_permissions = ()
        unique_together = (("db_server", "db_name"))
        verbose_name = '数据库管理'   
        verbose_name_plural = '服务器数据库信息'
        
    def to_json(self):      
        json_format = {
            "id":self.id,
            "db_name":self.db_name,
            "db_size":self.db_size,
            "ip":self.db_server.db_assets.server_assets.ip ,
            "db_port":self.db_server.db_port,
            "db_mark":self.db_server.db_mark,
            "db_size":self.db_size,
            "db_env":self.db_server.dataMap["env"][self.db_server.db_env],  
            "db_rw":self.db_server.dataMap["rw"][self.db_server.db_rw],            
            "count": 0
        }
        return  json_format 

    def to_connect(self):
        json_format = {
            "db_name":self.db_name,
            "ip":self.db_server.db_assets.server_assets.ip ,
            "db_port":self.db_server.db_port,
            "db_user":self.db_server.db_user,
            "db_passwd":self.db_server.db_passwd,  
        }
        return  json_format 
             
class Database_Table_Detail_Record(models.Model):
    db = models.SmallIntegerField(verbose_name='db_id')
    table_name = models.CharField(max_length=100,verbose_name='数据库表名',blank=True,null=True)    
    table_size = models.IntegerField(verbose_name='表大小',blank=True,null=True)
    table_row = models.IntegerField(verbose_name='行数大小',blank=True,null=True)
    last_time = models.IntegerField(verbose_name='记录时间',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_database_table_detail'
        default_permissions = ()
        index_together = ("db", "table_name")
        verbose_name = '数据库管理'   
        verbose_name_plural = '服务器数据库表记录信息'
    
class Database_User(models.Model):
    db = models.SmallIntegerField(verbose_name='db_id')
    user = models.SmallIntegerField(verbose_name='用户id') 
    tables =  models.TextField(verbose_name='可以操作的表',blank=True,null=True) 
    privs = models.CharField(max_length=250,verbose_name='SQL类型',blank=True,null=True)    
    class Meta:
        db_table = 'opsmanage_database_user'
        default_permissions = ()
        unique_together = (("db", "user"))
        verbose_name = '数据库管理'   
        verbose_name_plural = '用户数据库分配表'        

    def to_json(self):
        try:
            dbInfo = Database_Detail.objects.get(id=self.db)
        except:
            return  {
                        "id":self.id,
                        "db_name":"未知",
                        "db_size":"未知",
                        "count": 0
                    }
                    
        json_format = {
            "id":self.id,
            "dbIds":self.db,
            "db_name":dbInfo.db_name,
            "db_size":dbInfo.db_size,
            "tables":self.tables,
            "privs":self.privs,
            "count": 0
        }
        return  json_format 
    
class Database_Group(models.Model):
    db = models.SmallIntegerField(verbose_name='db_id')
    group = models.SmallIntegerField(verbose_name='用户id')    
    class Meta:
        db_table = 'opsmanage_database_group'
        default_permissions = ()
        unique_together = (("db", "group"))
        verbose_name = '数据库管理'  
        verbose_name_plural = '用户组数据库分配表'


class SQL_Execute_Histroy(models.Model):
    exe_user = models.CharField(max_length= 100,verbose_name='执行人')
    exe_db = models.ForeignKey('Database_Detail',verbose_name='数据库id', on_delete=models.CASCADE)
    exe_sql =  models.TextField(verbose_name='执行的SQL内容') 
    exec_status = models.SmallIntegerField(blank=True,null=True,verbose_name='执行状态')
    exe_result = models.TextField(blank=True,null=True,verbose_name='执行结果') 
    exe_time = models.IntegerField(default=0,verbose_name='执行时间')
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')  
    class Meta:
        db_table = 'opsmanage_sql_execute_histroy'
        default_permissions = ()
        permissions = (
            ("database_read_sql_execute_histroy", "读取SQL执行历史表权限"),
            ("database_change_sql_execute_histroy", "更改SQL执行历史表权限"),
            ("database_add_sql_execute_histroy", "添加SQL执行历史表权限"),
            ("database_delete_sql_execute_histroy", "删除SQL执行历史表权限"),              
        )
        verbose_name = '数据库管理'  
        verbose_name_plural = 'SQL执行历史记录表'     
        
class Custom_High_Risk_SQL(models.Model):
    sql = models.CharField(max_length=200,unique=True,verbose_name='SQL内容') 
    class Meta:
        db_table = 'opsmanage_custom_high_risk_sql'
        default_permissions = ()
        permissions = (
            ("database_read_custom_high_risk_sql", "读取高危SQL表权限"),
            ("database_change_custom_high_risk_sql", "更改高危SQL表权限"),
            ("database_add_custom_high_risk_sql", "添加高危SQL表权限"),
            ("database_delete_custom_high_risk_sql", "删除高危SQL表权限"),              
        )
        verbose_name = '数据库管理'   
        verbose_name_plural = '自定义高危SQL表' 
        
        