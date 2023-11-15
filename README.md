# BetterCalendar-API  
  
To run:  
1. Clone the directory:  
`git clone https://github.com/Szade-Organization/BetterCalendar-API.git`  
2. Create a .env file looking like this:  
> SECRET_KEY=your_secret_key  
.env for the development purposes file has been sent to you.  
Remember to never share the secret key, and not to push the .env file to the repository - it is already in .gitignore by default.
3. Run the setup script:  
`./setup`  
4. Run the server:  
`./run`  
4. Test if it works:  
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
  
  You can also use other methods such as fetch or curl.