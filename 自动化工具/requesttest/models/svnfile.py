from models.db import db, EntityModel


class DepartmentFolder(EntityModel):
    department = db.Column(db.String(250))          # 部门名字
    projectname = db.Column(db.String(250))         # 项目名字
    projectnum = db.Column(db.Integer)              # 项目数量
    departmentadmin = db.Column(db.String(250))     # 部门管理员
    status = db.Column(db.Integer)                  # 部门状态


class Project(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    name = db.Column(db.String(100))                # 项目名字
    description = db.Column(db.String(1000))        # 项目描述
    status = db.Column(db.Integer, default=ACTIVE)  # 项目状态
    weight = db.Column(db.Integer, default=1)
    ext = db.Column(db.Text())
    logo = db.Column(db.String(2048))               # 项目图标
    department = db.Column(db.String(250))          # 所属部门
    catalogue_info = db.Column(db.Text())           # 目录信息