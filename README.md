# CS50W Final Project

For my final project, I buit an e-commerce appliction. 
It handles everything from uploading the products, to viewing them, to adding to the cart, placing orders and making payments.

## Files I created
- `media` folder: Contains images images uploaded to the store
- `staticfiles/store` folder
    - `store.js` file: Contains `javascript` and `jquery` code for frontend manipulation
    - `styles.css` file: Contains `CSS` code for styling different parts of the application
- `store` folder
    - `urls.py` file: To connect the apps directories to the project level urls.py
    - `templates/store` folder
        - `cart.html`: To view items in cart, if any.
        - `index.html`: The home page of the app, that contains the listings in the store
        - `layout.html`: Holds the basic structure and design of each webpage
        - `login.html`: Contains html that handles login logic for users
        - `operator.html`: Holds the page to add product to the store
        - `register.html`: Holds the signup page for the store

## Running My Application
- `pip install -r requirements.txt` - This is to install dependencies
- `python manage.py makemigrations` - This is to make required migrations
- `python manage.py migrate` - This is to make the
- `python manage.py createsuperuser` (This step is not required)

## Distinctiveness and Complexity

1. An operator's dashboard to upload entries to the store
1. File handling to provided images for the entries
1. Payment pocessing through external API
1. Full system of an e-commerce application

## Other Information
1. Other files included like the `Procfile`, `.gitignore`  and `.env` files are created to host the application online
