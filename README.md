# Mini Taobao

A flask implementation that incorporates most of the features and functions found in Amazon's business model.

## Running/Stopping the Website

To run your website, in the Virtual Machine, go into the repository directory and issue the following commands:
```
db/setup.sh
source env/bin/activate
flask run
```
The first command sets up a database 

The next command will activate a specialized Python environment for running Flask.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```
## Description and Assumptions

Our implementation of Mini Taobao focusses on highlighting several features of an ecommerce site.

<h3>Login and Registration</h3>
Our implementation focuses on showcasing how a user can register and login by safely storing credentials in our database.
We assume that upon registering - a new seller and buyer account is created for each user, so that each user may act as buyer or seller. However, to separate these profiles out we implement a separate login process where the user must select their role. We also check to ensure that login credentials are valid and unique by rejecting duplicate emails. 

A user can add and remove balance from account. 
Every user has a personal profile page( visible after login that showcases imporant information) A user also has a public page that is accessible to all that hides sensitive information but allows one to see their public profile. 

<h4>Buyer</h4>

Any user logged in as a buyer can add products to cart, checkout, create a purchase and see their history of purchases including spending by category. 

<h4>Seller</h4>

Any user logged in as a seller can add products to inventory, create new products, and fulfil orders. 
Sellers can also see the sales by category and also other summary information on sales. Sellers may also access their reviews and ratings.

<h3>Cart and Checkout</h3>

Any buyer can add products to cart after browsing for products. A cart is implemented to store information on products a user may want to checkout that stores state, a user may freely add or delete products to cart. 


<h3>Product</h3>

Al products are categorized and we have an interface so that a guest may browse through the product catalog. However, to add a product to cart the guest must make a user profile. All sellers can add products and every product lists all the sellers that offer the product including the inventory size for every seller. Products can be searched by keyword, or by category. 


<h3>Inventory</h3>
We store inventory for each seller to include the products every seller has in stock. Sellers can update inventory by adding new quantities of products.

<h3>Orders</h3>

An order is implemented as a single item purchase with any quantity. Upon checkout of the cart, every unique item fulfilled by a specific seller is recorded as an order. 

<h3>Purchases</h3>

A purchase is a checkout of the cart, and included multiple orders. It can have different quantities of different types of products. 

<h3>Reviews</h3>

Any buyer can add reviews for a seller or a product. A review also consists of a rating that we use to summarize average ratings for seller and user. 

<h3>Analytics and visualizations</h3>

We showcase visualizations for the products that a user buys by category, we also show analytics to the seller on their most popular products, and the categories that are most succesful

We have also implemented a basic recommendation system that takes a users preferred product set and based on that looks at the most relevant categories to suggest products that are in these categories and are also part of the 50 most sold products on the platform. 


<h3>Data generation</h3>

We generate data using python libraries that allow us to create fake data. We also ensure all our data is connected based on our database schema and ensure that we generate 1000 users, reviews, products etc. to emulate a real online comerce platform. Our data generation process allows us to generate very large datasets. 


## Codebase

Our codebase is organized as follows :

app\
|   models\
|   static\                 
|   templates\

db\                         
|   data\
|   generated\


Our `app` directory contains the `models` directory that use SQL commands to draw data from the backend database. Each file in the `models` draws data from the SQL backend for a section of the implementation such as `product.py` for product related implementation, `seller.py` for seller related implementation, and similarly `user.py`, `review.py` etc for eponymous implementations. The frontend routing is done on the main directory in app where we have all our <b>api</b> endpoints setup using FLASK. 

All our data is generated in the `db` directory. Under `generated` we have `gen.py` and `gen2.py` that generate the data.


## Sample database
A sample database can be created and populated by db/generated/gen.py file and db/generated/./setup.sh. 



