# kivy-sql-demo
#### Works with mysql

### How to run:
1. ``` pip install -r requirements.txt ```
2. Change content of ```.env``` file with your credentials to access mysql locally:

    Example ```.env ``` file content
    ```
    DB_HOST=host_here
    DB_USER=user_here
    DB_PASSWORD=password_here
    ```
    change to your credentials:
    ```
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=pass
    ```
   
3. Run ```main.py``` file