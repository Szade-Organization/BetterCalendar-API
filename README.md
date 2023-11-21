# BetterCalendar-API  
  
To run:  
1. Create a desired folder.
2. Create a .env file:  
.env for the development purposes file has been sent to you.  
**Remember to never share the secret key, and not to push the .env file to the repository - it is already in .gitignore by default.**  
Your .env file should look like this:  
    > SECRET_KEY=your_secret_key
    > BC_DB_CONNECTION_STRING=your_connection_string
3. If you haven't login to ghcr from docker:  
   `docker login ghcr.io`  
   Remember you have to use your github token.  
4. Download/Copy paste the setup.sh script and add proper permissions (`chmod +x setup`).  
5. Run the setup script.  
    `./setup.sh`

6. Test if it works:  
Using httpie:  
`http GET 127.0.0.1:8000/api/info`  
    > HTTP/1.1 200 OK  
    > Allow: GET, HEAD, OPTIONS  
    > Content-Length: 152  
    > Content-Type: application/json  
    > Cross-Origin-Opener-Policy: same-origin    
    > Date: Wed, 15 Nov 2023 12:48:45 GMT  
    > Referrer-Policy: same-origin  
    > Server: WSGIServer/0.2 CPython/3.11.6  
    > Vary: Accept, Cookie  
    > X-Content-Type-Options: nosniff  
    > X-Frame-Options: DENY  
    >   
    > {  
    >     "api_name": "BetterCalendar-API",  
    >     "description": "An API for BetterCalendar project. Currently in development - this is the only view.",  
    >     "version": "0.0.1"  
    > }
    
    You can also use other methods such as curl:  
   `curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/info`
