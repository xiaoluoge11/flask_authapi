import gitlab

class GitLab:
    def __init__(self, url,token):
        self.gl = gitlab.Gitlab(url, private_token=token)
    
    def get_user_id(self, username):
        user = self.gl.users.list(username=username)[0]
        return user.id

    def get_group_id(self, groupname):
        group = self.gl.users.search(groupname)
        return group[0].id

    def get_by_members(self,name,repo,projectid):
        ret = []
        project = self.gl.projects.get(projectid)
        members = project.members.list()
        for i in members:
            ret.append(i.username)
            result={'name':name,'repo':repo,'user':ret,'id':projectid} 
        return result
    
    def get_project_id(self,name):
        projects = self.gl.projects.list(all=True)
        for project in projects:
            if project.name == name:
                return project.id

    def get_all_projects(self):
        projects = self.gl.projects.list(owned=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list

    def get_user_projects(self, username):
        ret=[]
        projects = self.gl.projects.list(owned=True) 
        for project_data in projects:
            data = self.get_by_members(project_data.name,project_data.http_url_to_repo,project_data.id) 
            if username in data['user']: 
                ret.append({'id':data['id'],'repo':data['repo'],'name':data['name']})
        return ret

    def get_group_projects(self, groupname):
        projects = self.gl.projects.owned(groupname=groupname, all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list
 

    def get_projects(self):
        projects = self.gl.projects.list(all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list

    def get_project(self,project_id):
        return self.gl.projects.get(project_id)

    def get_project_tag(self,project_id):
        project = self.get_project(project_id)
        data = [ i.name for i in project.tags.list()]
        return data

    def get_name_project(self,username):
        return self.gl.projects.list() 

    def project_members_create(self):
        return ({'user_id': user.id, 'access_level':gitlab.DEVELOPER_ACCESS})

    def create_user(self,email,password,username,name):
        user = self.gl.users.create({'email':
                                     email,'password':password,'username':username,'name': name})
        return user

    def user_list(self):
        return self.gl.users.list()


if __name__ == "__main__":
    gl=GitLab('http://10.10.1.78','NzsUZNa9M7sxY6q2Lg3Z')
    #data = gl.create_user('luohui@guangxi.beidou.cn','luohui123456','xiaoluoge11','xiaoluoge11')
    #print(gl.user_list()[0]) 
    print(gl.get_project_tag(1)) 
