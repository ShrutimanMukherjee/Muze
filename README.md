# Muze
Basic Music App using Flask framework

## Required python packages
- `flask`
- `flask_restful`
- `flask_sqlalchemy`

## Execution
Navigate to proect root
```bash
python app.py
```

## REST API
1. `/api/stat`
    - GET
        + request header : none
        + response :
            ```json
            {
                "n_songs" : type int,
                "n_albums" : type int,
                "n_users" : type int,
                "n_creators" : type int
            }
            ```
        + cURL Eg. `` curl -X GET http://127.0.0.1:8080/api/stat ``

2. `/api/user`
    - PUT
        + request header :
            ```json
            {
                "name" : type string,
                "password" : type string,
                "new_password" :type string 
            }
            ```
        + response :
            1. **Success**
                ```json
                {
                    "Message" : "Password Changed Successfully"
                }
                ```
            
            2. **Input error**
                ```json
                {
                    "Error" : "Incorrect Password or Invalid User"
                }
                status code : 400
                ```

            3. **Server Error**
                ```json
                {
                    "Error" : "Internal Server Error"
                }
                status code : 500
                ```
                
        + cURL Eg. `` # curl -X PUT http://127.0.0.1:8080/api/user -H "Content-Type: application/json" -d "{\"name\": \"<uname>\", \"password\":\"<oldpwd>\", \"new_password\":\"<newpwd>\"}" ``

3. `/api/user/<string:p_name>`
    `p_name` : parameter for user name
    - GET
        + request header : none
        + response :
            ```json
            {
                "name" : type string,
                "creator" : type boolean,
                "n_songs" : type int,
                "n_albums" : type int
            }
            ```
        + cURL Eg. `` curl -X GET http://127.0.0.1:8080/api/user/<string:p_name> ``

4. `/api/song/<string:p_name>`
    `p_name` : parameter for song name (use '%20' for space)
    - GET
        + request header : none
        + response :
            ```json
            {
                "name" : type string,
                "singer": type string,
                "genre": type string,
                "lyrics": type string,
                "release_date": type string,
                "rating": type float,
                "n_rating": type int
            }
            ```
        + cURL Eg. `` curl -X GET http://127.0.0.1:8080/api/song/<p_name> ``

5. `/api/all_songs`
    - GET
        + request header : none
        + response :
            ```json
            [
                {
                    "name" : type string,
                    "singer": type string,
                    "genre": type string,
                    "lyrics": type string,
                    "release_date": type string,
                    "rating": type float,
                    "n_rating": type int
                }
            ]
            ```
        + cURL Eg. `` curl -X GET http://127.0.0.1:8080/api/all_songs ``

## Further tasks
1. Pending features
    - view, edit playlist
    - useful data and charts on admin dashboard

2. Bugs to be fixed
    - Song_playlist relational table does not get updated

3. Features that can be added/improved
    - REST api
    - multi user
    - delete user accont
    - improved styling
    - back to home button