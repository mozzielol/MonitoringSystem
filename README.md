# MonitoringSystem
Remote Monitoring System based on Intel Edison. The code related to MongoDB and login function have been commented out. If you want to use these two function please create a account in [mlab](https://mlab.com/). After then, set the configuration in ./app/__init__.py. Finally, uncomment the code. Notice: No matter what is the name of your database, make sure there at least one document with the attribute 'username:yourusername' and 'password:yourpassword', or you cannot login.

USAGE: Download the code and run on Intel Edison. If you want to enable face recognition function, please direct to app/data/at. After then, run gen.py as python gen.py person's_name. It will create a directory with the faces detected. Make sure there are at least 10 images. 

This is the home page of the system(with all the function).

![alt text](https://github.com/mozzielol/MonitoringSystem/blob/master/Homepage.png)
