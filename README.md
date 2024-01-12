# Muze
Flask Music App

## Required python packages
- `flask`
- `flask_restful`
- `flask_sqlalchemy`

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
