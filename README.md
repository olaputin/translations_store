Translation Store

Microservice for storing and getting language package for POS client. 


1. Uploading. 
All language packages have to submitted to this repository for releases.
Format branches: `release/2.31` - for release 2.31, 


2. Getting. 
Pos client send get request and get json with language pack.
example of request: `http://0.0.0.0:8080/resources/LanguagePackageItem/?code=DE&version=2.29.000`