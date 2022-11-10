#!/bin/sh
#
rm deployment.zip

pip install --target ./packages -r requirements.txt

cd packages 

zip -r ../deployment.zip .

cd ..

zip deployment.zip lambda_function.py