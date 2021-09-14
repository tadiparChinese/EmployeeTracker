# Employee Tracking System

<<<<<<< HEAD
    ## Following functionalities need to be implemented
=======
  ## Following functionalities need to be implemented
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442

     1. Fixed start time - 9 AM
     2. Fixed end time - 6 PM

     3. No of times logged in - in perticular duration (count)
     4. No of times logged out - in perticular duration (count)

     5. List of Login times 
     6. List of Logout times

     7. Final status i.e. absent or present  if total_hrs < fixed_end_hrs then absent

     8. Fixed window (end-start time) 9AM to 7PM => 10 Hrs

     9. Total duration user stayed logged in -> total login time (count)

     10. User id


<<<<<<< HEAD
    ## API: [method] [api uri]
    ```
    [post] http://127.0.0.1:8000/api/register/
=======
   ## API: [method] [api uri]
    ```
   [post] http://127.0.0.1:8000/api/register/
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442

    {
    "username":"john",
    "email":"john@gmail.com",
    "password":"1234"
    }
    ```

    ```
<<<<<<< HEAD
    http://127.0.0.1:8000/api/login/
=======
   http://127.0.0.1:8000/api/login/
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442

    {
    "username": "admin",
    "password": "Password@123"
    }

    it will return in response 

    {
    "expiry": "2021-09-13T11:56:44.924698Z",
    "token": "99a27b2ebe718a2f0db6224e55b622a59ccdae9cf66861c60979a25ffb4f133e"
    }
    ```

    ```
<<<<<<< HEAD
    http://127.0.0.1:8000/api/logout/
=======
   http://127.0.0.1:8000/api/logout/
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442

    it will logout the user
    ```



    ```
<<<<<<< HEAD
    http://127.0.0.1:8000/api/logoutall/
=======
   http://127.0.0.1:8000/api/logoutall/
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442

    logout all users
    ```

    gives user details
    ```
<<<<<<< HEAD
    http://127.0.0.1:8000/api/info/ 
    ```


    ## API desc: what does this api do
    ## API request payload/query params :
    ## API Response payload: 
    ## API Headers:
=======
   http://127.0.0.1:8000/api/info/ 
    ```


    # API desc: what does this api do
    # API request payload/query params :
    # API Response payload: 
    # API Headers:
>>>>>>> c1118cf07e647f3db2866320dacaaa6bf479e442
