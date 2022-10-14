-- CREATE TABLE Purchases(
--     uid INT UNIQUE NOT NULL REFERENCES Users(uid),
--     purchase_id INT UNIQUE NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     number_of_orders INT NOT NULL,
--     total_amount DECIMAL(12,2) NOT NULL,
--     status VARCHAR NOT NULL,
--     time_created timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
--     payment_type VARCHAR NOT NULL,
-- );

-- CREATE TABLE Orders(
--     uid INT UNIQUE NOT NULL REFERENCES Users(uid),
--     purchase_id INT UNIQUE NOT NULL REFERENCES Purchases(purchase_id),
--     order_id INT UNIQUE NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     number_of_items INT NOT NULL,
--     amount DECIMAL(12,2) NOT NULL,
--     status VARCHAR NOT NULL,
--     product_id INT UNIQUE NOT NULL REFERENCES Products(product_id)
-- );

-- CREATE TABLE Users (
--     uid INT UNIQUE NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     firstname VARCHAR NOT NULL,
--     lastname VARCHAR NOT NULL,
--     address VARCHAR NOT NULL,
--     email VARCHAR UNIQUE NOT NULL,
--     password VARCHAR NOT NULL,
--     balance DECIMAL(12,2) NOT NULL,
--     phone_number INT NOT NULL
-- );

-- CREATE TABLE Products(
--     product_id INT UNIQUE NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     category VARCHAR NOT NULL,
--     image VARBINARY(MAX) NOT NULL,
--     name VARCHAR NOT NULL,
--     description VARCHAR NOT NULL,
--     price DECIMAL(12,2) NOT NULL,
--     available BOOLEAN DEFAULT TRUE
-- );

-- CREATE TABLE Reviews (
--     review_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     content VARCHAR,
--     rating INT NOT NULL
-- );

-- CREATE TABLE SellerReviews (
--     review_id INT NOT NULL REFERENCES Reviews(review_id),
--     seller_id INT NOT NULL REFERENCES Sellers(seller_id),
--     seller_comments VARCHAR,
--     seller_rating INT
-- );

-- CREATE TABLE ProductReviews (
--     review_id INT NOT NULL REFERENCES Reviews(review_id),
--     product_id INT UNIQUE NOT NULL REFERENCES Products(product_id),
--     product_comments VARCHAR,
--     product_rating INT
-- );

-- CREATE TABLE Sellers (
--     seller_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
--     balance DECIMAL(12,2) NOT NULL,
--     firstname VARCHAR NOT NULL,
--     lastname VARCHAR NOT NULL,
--     address VARCHAR NOT NULL,
--     email VARCHAR UNIQUE NOT NULL,
--     password VARCHAR NOT NULL,
--     phone_number INT NOT NULL
-- );

-- CREATE TABLE Cart (
--     uid INT UNIQUE NOT NULL REFERENCES Users(uid),
--     product_id INT UNIQUE NOT NULL REFERENCES Products(product_id),
--     cart_quantity INT NOT NULL,
--     unit_price DECIMAL(12,2) NOT NULL
-- );

-- CREATE TABLE Inventories (
--     seller_id INT NOT NULL REFERENCES Sellers(seller_id),
--     product_id INT UNIQUE NOT NULL REFERENCES Products(product_id),
--     inventory_quantity INT NOT NULL
-- );

-- CREATE TABLE UsersPurchases (
--     uid INT UNIQUE NOT NULL REFERENCES Users(uid),
--     purchase_id INT UNIQUE NOT NULL REFERENCES Purchases(purchase_id)
-- );

-- CREATE TABLE PurchasesOrders (
--     purchase_id INT UNIQUE NOT NULL REFERENCES Purchases(purchase_id),
--     order_id INT UNIQUE NOT NULL REFERENCES Orders(order_id)
-- );

-- CREATE TABLE OrdersProducts (
--     order_id INT UNIQUE NOT NULL REFERENCES Orders(order_id),
--     product_id INT UNIQUE NOT NULL REFERENCES Products(product_id),
-- );

-- CREATE TABLE OrdersSellers (
--     order_id INT UNIQUE NOT NULL REFERENCES Orders(order_id),
--     seller_id INT NOT NULL REFERENCES Sellers(seller_id)
-- );

-- CREATE TABLE UsersOrders (
--     order_id INT UNIQUE NOT NULL REFERENCES Orders(order_id),
--     uid INT UNIQUE NOT NULL REFERENCES Users(uid)
-- );


-- DO NOT DELETE THESE COMMENTS
-- THEY ARE ORIGINAL SKELETON CODE THAT BUILDS

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
