# API service for abstract billing system

| [Русская версия](https://github.com/KonstErz/Test_task_API_for_billing_system/blob/master/README.ru.md) |

### The service is implemented using the Django tools, Django REST framework

---


# Database structure

The service database is represented by the following objects and models (http://localhost:8000/admin/)

## Application API Models

+ **CURRENCY**  
Has a field *Name* - currency name according to ISO 4217 in the form of a three-letter alphabetical code in upper case (USD, EUR, etc.)

+ **EXCHANGE RATE**  
It has fields:  
*Currency Numerator* (foreign key to the Currency model);  
*Currency Denominator* (foreign key to the Currency model);  
*Current Rate* - current rate of the numerator currency in relation to the denominator currency

+ **WALLET**  
It has fields:  
*ID* - unique wallet id (UUID - known only to the owner of the wallet);  
*Owner* - wallet owner (foreign key to the User model);  
*Balance* - current amount of funds in the wallet;  
*Сurrency* - wallet currency (foreign key to the Currency model)

## Authorization Tokens

+ **TOKENS**  
It has fields:  
*Key* - user authorization token created when a new user is registered in the system;  
*User* - username (foreign key to the User model);  
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

(http://localhost:8000/api/registration/)

Creates a new user in the system.
Returns the ID of the new user.

***Sample input content:***  
`{"username": "John", "email": "travolta54@domain.com", "password": "thmstdiffcltpasswd955"}`

where are the fields:  
*username* - desired user profile name in the system;  
*email* - E-mail address;  
*password* - password for user authorization in the system


2.	**LOGIN**

(http://localhost:8000/api/login/)

Authenticates the user in the system, logs the user into his profile, provides access to conduct other operations in the system. 
Returns the user's authorization token or error with status code 400 in case of authentication failure.

***Sample input content:***  
`{"username": "John", "password": "thmstdiffcltpasswd955"}`

where are the fields:  
*username* - user profile name in the system;  
*password* - password for user authorization in the system


3.	**WALLET CREATOR**

(http://localhost:8000/api/walletcreation/)

Creates a new wallet, the owner of which is identified by the name of the user profile in the system (username), with a default balance of 0 and with the currency selected by the user from the available list of currencies in the system database.
Returns the ID of the created wallet.

***Sample input content:***  
`{"currency": "usd"}`

where is the field *currency* - name of the desired wallet currency from the available list of currencies in the system database 


4.	**WALLET DEPOSIT**

(http://localhost:8000/api/walletdeposit/)

Replenishes the balance (amount of funds) of the wallet with the current wallet currency by the desired amount.
Returns a message about the replenishment of the wallet balance by the desired amount.

***Sample input content:***  
`{"wallet_id": "029f7ead-dc0e-410d-91cf-873e92d2b999", "amount": 5000}`

where are the fields:  
*wallet_id* - wallet ID (in UUID4 format), the balance of which the user wishes to replenish;  
*amount* - the amount of funds to replenish the wallet balance


5.	**CONVERSION**

(http://localhost:8000/api/conversion/)

Transfers the specified amount of funds from one user's wallet to another wallet. If the currencies of the two wallets are different, then the funds are converted taking into account the current internal rate of the system for this currency pair.
Returns a message about a successful money conversion or an error with status code 400 in case of a lack of funds (if the user indicated an amount exceeding the current balance on his wallet).

***Sample input content:***  
`{"first_wallet_id": "029f7ead-dc0e-410d-91cf-873e92d2b999", "second_wallet_id": "acc65b3f-8944-4781-bc13-61f9eb8f2111", "amount": 500}`

where are the fields:  
*first_wallet_id* - wallet ID (in UUID4 format), the balance of which will decrease by the indicated amount of funds during conversion;  
*second_wallet_id* - wallet ID (in UUID4 format), the balance of which will be replenished by the indicated amount of funds during conversion;  
*amount* - amount of funds to be converted


6.	**TRANSACTION**

(http://localhost:8000/api/transaction/)

It transfers the specified amount of funds from the wallet of one user to the wallet of another user.
In the event that the currency of the sender’s wallet does not coincide with the currency of the recipient’s wallet, it automatically converts funds taking into account the current internal rate of the system for this currency pair. 
Returns a message about a successful transaction of funds or an error with status code 400 in case of a lack of funds (if the user indicated an amount exceeding the current balance on his wallet).

***Sample input content:***  
`{"username": "Uma", "currency": "usd", "my_wallet_id": "029f7ead-dc0e-410d-91cf-873e92d2b999", "amount": 2500}`

where are the fields:  
*username* - the name of the user profile in the system by which the wallet is identified, the balance of which will be replenished by the specified amount of funds during the transaction;  
*currency* - currency name of the wallet, the balance of which will be replenished by the indicated amount of funds during the transaction;  
*my_wallet_id* - wallet ID (in UUID4 format), the balance of which will decrease by the indicated amount of funds during the transaction;  
*amount* - the amount of funds to be transacted

---


### Service Features


***Advantages***

+ All operations related to wallets can be carried out only by users who are authorized in the system;
+ Handling most common errors related to incorrect data entry;
+ Currency name input is not case sensitive;
+ Correct arithmetic rounding of funds on the wallet balance when replenishing the wallet balance, converting and transactions of funds;
+ The ability to automatically convert funds when transaction of funds to another user.


***Flaws***
+ When a user replenishes a wallet balance, the possibility of distinguishing between the foreign currency and the current wallet currency should be taken into account, and if necessary, the payment will be converted automatically;
+ The internal exchange rate in the system, ideally, should be constantly kept up to date due to requests for an external API with the current exchange rates in the world (such services are provided, for example [TCB RF](https://www.cbr.ru/development/DWS/), [European CB](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml), [Bloomberg](https://www.bloomberg.com/markets/currencies) and etc.);
+ The format for displaying the user's wallet balance (for example, a float num rounded to the second digit after the period) must be constant both when replenishing the balance and as a result of money conversion and transaction operations, and should not depend on the format of a currency value;
+ Tests(!): at the moment, application endpoint test coverage is 0%. As a result of which, support for the code base is greatly complicated when the service doesn't work as a result of changes to the code :(
 
---


### Quick start guide for starting a service on your local computer

1.	This project exists as a docker container, for its correct mounting and launch on your local computer you will need to install the current version of the [Docker Engine](https://docs.docker.com/engine/install/) (ver. from *17.06.0* and higher).

2. To build a Docker image, you need files with environment variables *env.project* and *env.db*. So rename the files *env.project.example* and *env.db.example* from the repository accordingly. These files contain variables for the correct operation of the project. You can change the values of the variables to suit your needs.

3.  To mount the image, from the project root folder, run the following command in the terminal:

    ```
    docker-compose build
    ```

4.  After successfully installing all the necessary requirements, start the container:

    ```
    docker-compose up -d
    ```

5.  With the following command you can create a superuser:

    ```
    docker-compose exec web python manage.py createsuperuser
    ```

6.  Now you can go to the server http://localhost:8000/ in your browser. Sign in under the credentials of the superuser you created (http://localhost:8000/admin/ or at http://localhost:8000/api/login/) and try to create several test objects of each type in the project admin panel. You can test the operation of the main functionality of the application, for example: creating a wallet (http://localhost:8000/api/walletcreation/), replenishing the balance (http://localhost:8000/api/walletdeposit/) and transaction of funds to another user (http://localhost:8000/api/transaction/).


Other useful commands that may come in handy when working with the docker container of the project:
    
    docker-compose logs -f    # Logs of running services (Ctrl+C - exit)
    
    docker-compose down -v   # Remove the volumes along with the containers
    
    docker images       # List all running images
    docker images -a    # List all images
    
    docker ps       # List all running containers
    docker ps -a    # List all containers
    
    docker stop $(docker ps -a -q)      # Stop all containers
    docker rm $(docker ps -a -q)     # Remove all containers

    docker rm <ID_or_Name>    # Removing a specific container by ID or name
    
    docker rmi $(docker images -f dangling=true -q)    # Remove all images not tagged
    
    docker rmi <Image_ID>    # Removing a specific image by ID
    
    docker rmi $(docker images -a -q)    # Remove all images
    
    docker rmi -f $(docker images -a -q)    # Forced removing of all images
    
