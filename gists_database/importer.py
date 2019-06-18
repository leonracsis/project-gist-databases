import requests
import json
import sqlite3

def import_gists_to_database(db, username, commit=True):
    
    print(username)
    req_str = 'https://api.github.com/users/{}/gists'.format(username)
    resp = requests.get(req_str)
    print (resp.status_code)
    if resp.status_code==404:
        raise requests.exceptions.HTTPError        
        
    gists_list = resp.json()
    db.executescript("""
    DROP TABLE if exists gists;
    CREATE TABLE gists (
      id INTEGER PRIMARY KEY autoincrement,
      github_id TEXT NOT NULL,
      html_url TEXT NOT NULL,

      git_pull_url TEXT NOT NULL,
      git_push_url TEXT NOT NULL,

      commits_url TEXT NOT NULL,
      forks_url TEXT NOT NULL,

      public BOOLEAN NOT NULL,

      created_at DATETIME NOT NULL,
      updated_at DATETIME NOT NULL,

      comments INTEGER NOT NULL,
      comments_url TEXT NOT NULL
    );
    """)
   
    insert_str = """
    INSERT INTO gists 
        (github_id, 
        html_url, 
        git_pull_url, 
        git_push_url, 
        commits_url, 
        forks_url, 
        public, 
        created_at, 
        updated_at, 
        comments, 
        comments_url)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """

    for gist_rec in gists_list:       
        db.execute(insert_str,                  
                  (gist_rec['id'],
                   gist_rec['html_url'],
                   gist_rec['git_pull_url'],
                   gist_rec['git_push_url'],
                   gist_rec['commits_url'],
                   gist_rec['forks_url'],
                   gist_rec['public'],
                   gist_rec['created_at'],
                   gist_rec['updated_at'],
                   gist_rec['comments'],
                   gist_rec['comments_url'] ))

    if commit:
        db.commit()