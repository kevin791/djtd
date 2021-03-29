from pathlib import Path
from flask import current_app
from models.svnfile import (DepartmentFolder, Project)


class GetUploadFile(object):
    # 递归传过来的路径下所有文件
    @classmethod
    def searchAllFiles(cls, path, fileTree, initial=True):
        if initial:
            root = path if isinstance(path, str) else str(path)
            fileTree[root] = {}
            initial = False
            return cls.searchAllFiles(root, fileTree[root], initial)
        p = Path(path if isinstance(path, str) else str(path))
        dirs = [x for x in p.iterdir() if x.is_dir()]
        files = [x for x in p.iterdir() if x.is_file()]
        for file in files:
            fileTree[file.name] = [file.suffix, file.as_posix()]
        for dir in dirs:
            fileTree[str(dir.parts[-1])] = {}
            cls.searchAllFiles(dir, fileTree[str(dir.parts[-1])], initial)

    # 返回前端请求的方法
    @classmethod
    def myfloderpath(cls):
        # 定义一个路径，后期这里需要替换成配置文件中的路径
        sampleDir = 'E:\svn'
        fileTree = {}
        cls.searchAllFiles(sampleDir, fileTree)
        # 定义一个数组，用来转换searchAllFiles方法中的数据结构
        floadlist = []
        # 遍历fileTree字典，将遍历出来的数据重新添加到一个新数组中
        for fload1 in fileTree.values():
            for key, value in fload1.items():
                floadlist.append(
                    {
                        "department": key,
                        "floade": cls.projectlist(value)
                        # "floade": value
                    }
                )
        # 返回给前端
        return floadlist

    # 遍历项目的方法，将传过来的字典重新组合成一个新的数组，以达到预期的数据结构
    @classmethod
    def projectlist(cls, disc):
        projectlist = []
        if isinstance(disc, dict):
            for key, value in disc.items():
                projectlist.append(
                    {
                        "projectname": key
                    }
                )
        return projectlist

    @classmethod
    def updateproject(cls, db):
        data = GetUploadFile.myfloderpath()
        print(data)

        for dp in data:
            department = dp['department']
            if department[0:5] == "游戏申测_":
                department = department.split("游戏申测_")[1]
            project = cls.allprojectlist(dp['floade'])
            projectnum = len(project.split(","))
            departmentadmin = "林映旭"
            res = db.session.query(DepartmentFolder).filter(DepartmentFolder.department == department).first()
            if department[0] != ".":
                if res:
                    dpres = db.session.query(DepartmentFolder).get(res.id)
                    dpres.department = department
                    dpres.projectname = project
                    dpres.projectnum = projectnum
                    dpres.departmentadmin = departmentadmin
                    dpres.status = 1
                    db.session.add(dpres)
                    db.session.commit()
                else:
                    cls.creat_department(department, project, projectnum, departmentadmin, db)
            for pro in project.split(","):
                pres = db.session.query(Project).filter(Project.name == pro).first()
                if pro != "" and pro[0] != ".":
                    if pres:
                        prores = db.session.query(Project).get(pres.id)
                        prores.name = pro
                        prores.status = 0
                        prores.department = department
                        prores.catalogue_info = str(cls.getprojectflold(pro, department))
                    else:
                        catalogue_info = str(cls.getprojectflold(pro, department))
                        # catalogue_info = "test"
                        cls.creat_project(pro, "", 0, 1, "", department, db, catalogue_info)
                else:
                    print("过滤空文件和隐藏文件夹")
        return data

    # 返回前端请求的方法
    @classmethod
    def getprojectflold(cls, project, department):
        # 定义一个路径，后期这里需要替换成配置文件中的路径
        sampleDir = 'E:\svn'
        if department[0] != ".":
            newdir = sampleDir + '/' + '游戏申测_' + department + '/' + '游戏申测_' + project
            fileTree = {}
            cls.searchAllFiles(newdir, fileTree)
            # # 定义一个数组，用来转换searchAllFiles方法中的数据结构
            # floadlist = []
            # # 遍历fileTree字典，将遍历出来的数据重新添加到一个新数组中
            # for fload1 in fileTree.values():
            #     for key, value in fload1.items():
            #         floadlist.append(
            #             {
            #                 "department": key,
            #                 "floade": cls.projectlist(value)
            #                 # "floade": value
            #             }
            #         )
            # 返回给前端
            return fileTree

    @classmethod
    def allprojectlist(cls, floade):
        allproject = ""
        for list in floade:
            if list['projectname'][0] != ".":
                if list['projectname'][0:5] == "游戏申测_":
                    splist = list['projectname'].split("游戏申测_")[1]
                    allproject += splist + ","
                else:
                    allproject += list['projectname'] + ","
        allproject = allproject[: - 1]
        return allproject

    @classmethod
    def creat_department(cls, department, projectname, projectnum, departmentadmin, db):
        try:
            ret = db.session.query(DepartmentFolder).filter(DepartmentFolder.department == department).first()
            if ret:
                return 103, None
            dp = DepartmentFolder(
                department=department,
                projectname=projectname,
                projectnum=projectnum,
                departmentadmin=departmentadmin,
                status=1)
            db.session.add(dp)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def creat_project(cls, name, description, status, weight, logo, department, db, catalogue_info):
        try:
            ret = db.session.query(Project).filter(Project.name == name).first()
            if ret:
                return 103, None
            pr = Project(
                name=name,
                description=description,
                status=status,
                weight=weight,
                logo=logo,
                department=department,
                catalogue_info=catalogue_info)
            db.session.add(pr)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)



