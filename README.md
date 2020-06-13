# API service for abstract billing system

| [Русская версия](https://github.com/KonstErz/Test_task_API_for_billing_system/blob/master/README.ru.md) |

### The service is implemented using the Django tools, Django REST framework

---


# Database structure

The service database is represented by the following objects and models (http://.../admin/)

## Application API Models

+ **CURRENCY**
Has a field *Name* - currency name according to ISO 4217 in the form of a three-letter alphabetical code in upper case (USD, EUR, etc.)

+ **EXCHANGE RATE**
It has fields: 
*Currency Numerator*; 
*Currency Denominator*; 
*Current Rate* - current rate of the numerator currency in relation to the denominator currency

+ **WALLET**
It has fields: 
*ID* - unique wallet id; 
*Owner* - wallet owner (username user profile); 
*Balance* - current amount of funds in the wallet; 
*Сurrency* - wallet currency

## Authorization Tokens

+ **TOKENS**
It has fields: 
*Key* - user authorization token created when a new user is registered in the system; 
*User* - username (username user profile); 
*Created* - date and time of token creation (user registration in the system)

## Authentication and Authorization Data

+ **GROUPS** - groups of users

+ **USERS**
User profile has fields: 
*Username*; 
*Email Address*;
*First Name*; 
*Last Name*; 
*Staff Status* - defines user access rights in the system

---


# Application API Functionality

The service provides 6 basic functional units that support input in JSON format.


1.	**REGISTRATION**

(http://.../api/registration/)

Creates a new user in the system, a user authorization token in the system.
Returns the ID of the new user.

***Sample input content:***     `{"username": "John", "email": "travolta54@domain.com", "password": "thmstdiffcltpasswd955"}`

where are the fields: 
*username* - desired user profile name in the system; 
*email* - E-mail address;
*password* - password for user authorization in the system


2.	**LOGIN**

(http://.../api/login/)

Authenticates the user in the system, logs the user into his profile, provides rights to conduct other operations in the system. 
Returns the user authorization token or error with status code 400 in case of authentication failure.

***Sample input content:***     `{"username": "John", "password": "thmstdiffcltpasswd955"}`

where are the fields: 
*username* - user profile name in the system; 
*password* - password for user authorization in the system


3.	**WALLET CREATOR**

(http://.../api/walletcreation/)

Creates a new wallet, the owner of which is identified by the name of the user profile in the system (username), with a default balance of 0 and with the currency selected by the user from the available list of currencies in the system database.
Returns the ID of the created wallet.

***Sample input content:***     `{"currency": "usd"}`

where is the field *currency* - name of the desired wallet currency from the available list of currencies in the system database 


4.	**WALLET DEPOSIT**

(http://.../api/walletdeposit/)

Replenishes the balance (amount of funds) of the wallet with the current wallet currency by the desired amount.
Returns a message about the replenishment of the wallet balance by the desired amount or an error with the status code 400 if the user does not have a wallet.

***Sample input content:***     `{"currency": "usd", "amount": 300}`

where are the fields: 
*currency* - currency name of the wallet, the balance of which the user wishes to replenish;
*amount* - the amount of funds to replenish the wallet balance


5.	**CONVERSION**

(http://.../api/conversion/)

It transfers the specified amount of funds from the user's wallet with one currency to the user's wallet with another currency, while converting funds taking into account the current internal rate of the system for this currency pair.
Returns a message about a successful money conversion or an error with status code 400 in case of a shortage of funds (if the user indicated an amount exceeding the current balance on his wallet).

***Sample input content:***     `{"first_currency": "usd", "second_currency": "eur", "amount": 250}`

where are the fields: 
*first_currency* - currency name of the wallet, the balance of which will decrease by the indicated amount of funds during conversion;
*second_currency* - currency name of the wallet, the balance of which will be replenished by the indicated amount of funds during conversion;
*amount* - amount of funds to be converted


6.	**TRANSACTION**

(http://.../api/transaction/)

It transfers the specified amount of funds from the wallet of one user to the wallet of another user.
In the event that the currency of the sender’s wallet does not coincide with the currency of the recipient’s wallet, it automatically converts funds taking into account the current internal rate of the system for this currency pair. 
Returns a message about a successful transaction of funds or an error with status code 400 if the user does not have a wallet or in case of a lack of funds (if the user indicated an amount exceeding the current balance on his wallet)

***Sample input content:***     `{"username": "Uma", "currency": "usd", "my_wallet_currency": "usd", "amount": 250}`

where are the fields: 
*username* - the name of the user profile in the system by which the wallet is identified, the balance of which will be replenished by the specified amount of funds during the transaction;
*currency* - currency name of the wallet, the balance of which will be replenished by the indicated amount of funds during the transaction;
*my_wallet_currency* - currency name of the wallet, the balance of which will decrease by the indicated amount of funds during the transaction;
*amount* - the amount of funds to be transacted

---


### Service Features


***Advantages***

+ All operations related to wallets can be carried out only by users who are authorized in the system;
+ Handling most common errors related to incorrect data entry;
+ Currency name input is not case sensitive;
+ Correct arithmetic rounding of funds on the balance of the wallet during the operations of conversion and transaction of funds;
+ The ability to automatically convert funds when transaction of funds to another user.


***Flaws***
+ When a user replenishes a wallet balance, the possibility of distinguishing between the foreign currency and the current wallet currency should be taken into account, and if necessary, the payment will be converted automatically;
+ The internal exchange rate in the system, ideally, should be constantly kept up to date due to requests for an external API with the current exchange rates in the world (such services are provided, for example [TCB RF](https://www.cbr.ru/development/DWS/), [European CB](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml), [Bloomberg](https://www.bloomberg.com/markets/currencies) and etc.);
+ The format for displaying the user's wallet balance (for example, a float num rounded to the second digit after the period) must be constant both when replenishing the balance and as a result of money conversion and transaction operations, and should not depend on the format of a currency value;
+ With a high degree of probability, the code for processing the request for converting funds can be optimized in terms of speed and readability;
+ Tests(!): at the moment, application endpoint test coverage is 0%. As a result of which, support for the code base is greatly complicated when the service doesn't work as a result of changes to the code :(
 
---


### Quick start guide for starting a service on your local computer

1.	This project exists as a docker container, for its correct mounting and launch on your local computer you will need to install the current versions of the [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

2.  To mount the image, from the project root folder, run the following command in the terminal:

    ```
    docker-compose build
    ```

3.  After successfully installing all the necessary requirements, start the container:

    ```
    docker-compose up -d
    ```

4.  Before moving to the server, create a superuser in the system:

    ```
    docker-compose exec web python manage.py createsuperuser
    ```

Attention! The project already has a default SQLite database (db.sqlite3) preinstalled, and all the necessary migrations are created and applied.

5.  Now you can go to the server http://localhost:8000/ in your browser. Log in to the project admin panel (http://localhost:8000/admin/) under the credentials of the superuser you created and try to create several test objects of each type. You can test the operation of the main functionality of the application, for example: creating a wallet (http://localhost:8000/api/walletcreation/), replenishing the balance (http://localhost:8000/api/walletdeposit/) and transaction of funds to another user (http://localhost:8000/api/transaction/).


Other useful commands that may come in handy when working with the docker container of the project:
    
    docker images -a
    docker-compose images    # List all images
    
    docker ps -a
    docker-compose ps    # List all containers

    docker-compose logs -f    # Logs of running services

    docker-compose down   # Stop running containers

    docker rmi $(docker images -f "dangling=true" -q)    # Delete all images not tagged

    docker rmi <Image_ID>    # Delete a specific image by ID

    docker rmi $(docker images -a -q)    # Delete all images

    docker rm <ID_or_Name>    # Removing a specific container by ID or name

    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)     # Stop and delete all containers
    




