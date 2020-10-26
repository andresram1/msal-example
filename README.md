# Microsoft Authentication Library (MSAL) Example

## Introduction

This is a simplified example of the original one published here:
[Got to GitHub](https://github.com/Azure-Samples/ms-identity-python-webapp)

Please follow the instructions given in that repository in order to set up the App Registration


## Purpose of this example

The idea of this example is to remove the Flask complexity and to create a "kind of" functional API. Most of the 
original implementation relies on Flask using templates, but what if the client is implemented with some other 
technology such as Angular, React JS, etc. So, instead of making all the effort, then delegates part of the
responsibility to the client.

## How to use it?

Just follow the indications given in the original repository.

1. Make a call to the index (i.e. "/").
2. The index will redirect you if the session is not set (Or if the JWT is missing)
3. The API will give you the redirection URL.
4. The client will get the redirect URL and will call directly that URL.
5. The user will need to authenticate (or better, to authorize the access to this application)
6. MSAL will give the code
7. The client retrieves the code and make another call to the API (i.e. "/getAToken").
8. The API will check if the code is valid and will return the token

# Remarks

- It's just a starting point!
- Of course, this is an example. Is not intended to be in a production-like environment. Some other things need to be
reviewed/considered.

 

  
 