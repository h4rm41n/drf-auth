# drf-auth
## build drf using rest_framework.authtoken

#### Cara pemasangan (ubuntu os, virtualenv)
##### 1. clone repository 
~ git clone https://github.com/h4rm41n/drf-auth.git
##### 2. Buka terminal dan masuk ke direktori drf-auth
~ cd drf-auth
##### 3. Buat environment baru dengan perintah 
~ virtualenv env
##### 4. Aktifkan environment 
~ source env/bin/activated
##### 5. Masuk ke direktori src lalu install package 
~ pip install -r req.txt
##### 6. Buat database
~ ./manage.py migrate
##### 7. Buat userbaru
~ ./manage.py createsuperuser
##### 8. Jalankan project 
~ ./manage.py runserver
