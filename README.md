# CS50W Final Project

For my final project, I buit an e-commerce appliction.
It handles everything from uploading the products, to viewing them, to adding to the cart, placing orders and making payments.

## Files I created

- `media` folder: Contains images images uploaded to the store

- `staticfiles/store` folder
  - `store.js` file: Contains `javascript` and `jquery` code for frontend manipulation
  - `styles.css` file: Contains `CSS` code for styling different parts of the application

- `store` folder

  - `admin.py` file:
    1. Required imports are made including the ones from `models.py`
    2. A class is created to create a log of all actions performed on the site. It stores an ID, the user and the time the action was performed
    3. The models and the classes are registered to the admin interface

  - `apps.py` file:
      1. App configurations made in this file

  - `models.py` file

    1. Class `User` is created which inherits from the `AbstaractUser` class. The is to modify the default user model to suit the need of the app

    2. Model `Category` contains a field which holds different categories of items created on the site

    3. Model `Product` contains five fields that holds the properties of a product in the site
        - `category` - Foreign key field that references a single category
        - `description` - Text field for the description of the product
        - `id`: Uniquely identifies each product
        - `name`: Contains the name to be displayed for each product
        - `image`: Image field that stores what image should be displayed

    4. Model `Order` manages all orders made and contains three fields
        - `id`: Uniquely identifies each product
        - `user`: Foreign key field that tells which user ordered
        - `product`: Foreign key field that references the product ordered
        - `units`: Tells how many units were ordered

  - `urls.py` file:
      1. Import required functions from the views.py file
      2. A list `urlpatterns` is created that the directs to different parts of the website based on the functions in the views.

  - `views.py` file: Contains functions(views) for application logic
    1. `about`: Renders the `about.html`

    2. `add_category`: Performs logic to add a product category for the site
        - Checks the request type

        - If it is `POST`:
           1. Fetches the value to be added and stores it in a variable
           2. Creates a new `Category` model object with the value gotten
           3. Saves the model
           4. Redirects to `operator` url
        - If not, it goes to the `operator` url directly

    3. `add_to_cart`: Performs logic to add a product to a user's cart
        - Gets the model object by passing in `product_id` gotten from the function
        - Gets the model object for the current user
        - If the product is already in the user's cart fields, it would be removed
        - If not, it would be added
        - Then the user's model is saved
        - Finally, it redirects back to the product's page

    4. `cart`: Displays the contents of the user's shopping cart
        - The function retrieves the current user object
        - Retrieves all the products associated with the user's cart.
        - Retrieves all available categories from the database using `models.Category.objects.all()`.
        - The `render` function is used to generate an HTTP response with the rendered HTML template.
        - The template used is "store/cart.html".
        - The template context is populated with the following variables:
            - `cart_items`: Contains the list of products in the user's cart.
            - `show_side`: A variable that might control the visibility of a side section (details not provided).
            - `categories`: Contains all available product categories.

    5. `category`: displays products belonging to a specific category
       - Identifies the desired category by querying the database using the `id` of the specified category
       - Products belonging to the specified category are retrieved by applying a filter using
       - The `render` function is used to generate an HTTP response with the rendered HTML template.
       - The template used is "store/index.html".
       - The template context is populated with the following variables:
         - `products`: List of products in the specified category.
         - `categories`: List of all available categories.
         - `category_name`: Name of the current category.
         - `show_side`: A variable controlling side section visibility.

    6. `checkout`: Responsible for processing the checkout process and initiating payment for the items in the user's cart
       - The function retrieves the user's cart items using the logged-in user's ID
       - The function calculates the total price of items in the cart by iterating through each item and summing up their prices.
       - An API request is constructed to the Flutterwave payment endpoint, defined by the URL
       - The API request's authorization header is set using an API key retrieved from the environment variable
       - The API request includes a JSON payload with payment details such as transaction reference, total amount, currency, redirect URL, customer information, and customizations.
       - The constructed API request with the JSON payload is sent using the `requests.post` method.
       - The response from the API is received and its JSON data is processed.
       - If the payment status in the response data is "success," the user is redirected to the payment link provided in the response data.
       - If the payment status is not "success," the user is redirected to the homepage.
       - The function returns an HTTP response, either redirecting the user to the payment link (in case of successful payment initiation) or to the homepage (in case of payment failure).

    7. `index`: Renders the main page of the store, displaying all available products.
       - Retrieve all products from the database using `models.Product.objects.all()`.
       - Retrieve all available categories from the database using `models.Category.objects.all()`.
       - Render the "store/index.html" template with the following variables:
         - `products`: List of all products.
         - `categories`: List of all available categories.
         - `category_name`: A string representing the current category (set to "All Items").
         - `show_side`: A variable controlling side section visibility.
         - An HTTP response with the rendered HTML template, displaying all available products and categories.

    8. `generate_name` Helper function generates a unique filename to be stored
       - Retrieve the current date and time using `datetime.now()`.
       - Construct the filename using the provided `name`, current year, month, day, hour, minute, second, and the specified file extension `ext`.
       - Returns a string containing the generated filename in the specified format.

    9. `login_view`: Handles user authentication and login process.
       - Supports both GET and POST requests.
       - If the request method is "POST":
       - Retrieve the provided email and password from the POST data.
       - Attempt to authenticate the user using `authenticate(request, username=username, password=password)`.
       - If authentication is successful:
       - Log the user in using `login(request, user)`.
       - Redirect the user to the "index" view using `HttpResponseRedirect(reverse("index"))`.
       - If authentication fails:
       - Render the "store/login.html" template with an error message.
       - If the request method is not "POST":
       - Render the "store/login.html" template for user login.
       - For a successful login, it returns an HTTP redirect to the "index" view.
       - For unsuccessful login attempts, it returns an HTTP response rendering the "store/login.html" template with an error message.
       - The function uses Django's built-in `authenticate` and `login` methods to handle user authentication and session management.
       - The provided description offers an overview of the function's purpose, steps, and possible outcomes.

    10. `logout_view`: Handles user logout and session termination.
        - Logs the user out and redirects to the "index" view after successful logout.
        - Use the `logout(request)` function to terminate the user's session.
        - Redirect the user to the "index" view after successful logout.
        - The function utilizes Django's built-in `logout` method to handle user session termination.

    11. `order`: Initiates an order process for a specific product.
        - Retrieve the product object based on the provided `product_id`
        - Construct an API request to Flutterwave's payment endpoint
        - Set the necessary authorization header using the provided API key.
        - Create a JSON payload containing payment details such as transaction reference, product price, currency, user information, and customizations.
        - Send the API request using the `requests.post` method.
        - Process the response JSON data.
        - If the payment initiation is successful:
        - Redirect the user to the payment link provided in the response data.
        - If the payment initiation fails:
        - Redirect the user back to the product page.

    12. `operator`: Manages operations related to adding products by an operator user.
        - If the method is "POST":
          - Retrieve the category name, product name, description, price, and image file from the POST data.
          - Retrieve the corresponding `Category` object based on the category name.
          - Generate a new unique filename for the uploaded image using `generate_name` function.
          - Save the uploaded image to the specified file path.
          - Create a new `Product` object with the provided details and saved image filename.
          - Save the new product to the database.
          - Redirect the user back to the "operator" view.
        - If the method is not "POST":
          - Retrieve all products and categories from the database.
          - Render the "store/operator.html" template with the appropriate variables.

    13. `op_category`: Displays products of a specific category in the operator's view.
        - Retrieves products belonging to the specified category and displays them.
        - Retrieve the `id` of the specified category using the category name
        - Fetch products belonging to the specified category
        - Retrieve all available categories from the database
        - Render the "store/operator.html" template with the following variables:
          - `products`: List of products in the specified category.
          - `categories`: List of all available categories.
          - `category_name`: Name of the current category.
          - `show_side`: A variable controlling side section visibility.
        - Returns an HTTP response with the rendered HTML template, displaying products of the specified category in the operator's view.

    14. `op_remove`: Handles the removal of a product by an operator user.
        - Retrieves the product to be removed based on the provided `product_id`.
        - Delete the retrieved product from the database using the `delete` method.
        - Redirect the operator user back to the "operator" view using `HttpResponseRedirect(reverse("operator"))`.
        - Returns an HTTP redirect to the "operator" view after successful product removal.

    15. `product_view`: Displays details of a specific product along with an option to add or remove it from the user's cart.
        - Determines whether the product is already in the user's cart and adjusts the option text accordingly.
        - Retrieve all available categories from the database using `models.Category.objects.all()`.
        - Retrieve the current user object based on the logged-in user's username
        - Retrieves product details based on the provided `product_id`

        - Check if the retrieved product is already in the user's cart:
          - If yes, set the `add` variable to "Remove From Cart".
          - If no, set the `add` variable to "Add to Cart".
        - Render the "store/product.html" template with the following variables:
          - `product`: The details of the retrieved product.
          - `add`: Text indicating whether the product should be added or removed from the cart.
          - `categories`: List of all available categories.
          - `show_side`: A variable controlling side section visibility.

        - Returns an HTTP response with the rendered HTML template, displaying the details of the requested product

    16. `register`: Handles user registration process, allowing users to create new accounts.
        - Check the method type
        - If the method is "POST":
          - Retrieve the provided username, email, password, and password confirmation from the POST data.
          - Ensure that the password and confirmation match; if not, render an error message.
          - Attempt to create a new user account using
            - If successful, the user is saved to the database.
            - If unsuccessful due to a duplicate username, render an error message.
          - Log the user in using the `login` function.
          - Redirect the user to the "index" view
        - If the method is not "POST":
          - Render the "store/register.html" template for user registration.

        - For a successful registration, it returns an HTTP redirect to the "index" view.
        - For other cases, it returns an HTTP response rendering the "store/register.html" template

    17. `remove_from_cart`: Handles the removal of a product from the user's cart.
        - Retrieves the product to be removed based on the provided `product_id`.
        - Retrieve the current user object based on the logged-in user's username.
        - Remove the retrieved product from the user's cart using the `remove` method.
        - Save the user object to persist the changes.
        - Redirect the user to the `cart` view
        - Returns an HTTP redirect to the "cart" view after successful removal from the cart.

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
- `python manage.py migrate` - This is to migrate
- `python manage.py createsuperuser` (This step is not required)

## Distinctiveness and Complexity

1. An operator's dashboard to upload entries to the store
1. File handling to provided images for the entries
1. Payment pocessing through external API
1. Full system of an e-commerce application

## Other Information

1. Other files included like the `Procfile`, `.gitignore`  and `.env` files are created to host the application online
