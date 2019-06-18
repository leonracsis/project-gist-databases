from .models import Gist
from datetime import datetime

def search_gists(db_connection, **kwargs):

    parm_github_id=None
    parm_created_at=None
    
    for key, value in kwargs.items():        
        if key=='github_id':
            parm_github_id=value
        if key=='created_at':
            parm_created_at=value
            
    sel_str1 = 'SELECT *  FROM gists'
    
    if parm_github_id and parm_created_at:
        sel_str2 = ' WHERE github_id = ? and created_at = ?'
        select_str = sel_str1 + sel_str2
        result=db_connection.execute(select_str,(parm_github_id, parm_created_at))
        
    if parm_github_id and parm_created_at is None:
        sel_str2 = " WHERE github_id = '{}'"
        select_str = sel_str1 + sel_str2.format(parm_github_id)
        result=db_connection.execute(select_str)        
        
        
    if parm_github_id is None and parm_created_at:
        sel_str2 = " WHERE created_at = '{}Z'"
        select_str = sel_str1 + sel_str2.format(datetime.isoformat(parm_created_at))
        
        result=db_connection.execute(select_str)        

    if parm_github_id is None and parm_created_at is None:
        result=db_connection.execute(sel_str1)        

    result_list=[]
    for rec in result.fetchall():
        result_class = Gist(rec)
        result_list.append(result_class)
        
    return result_list
    