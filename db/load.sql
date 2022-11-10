\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_purchase_id_seq',
                         (SELECT MAX(purchase_id)+1 FROM Purchases),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellers_seller_id_seq',
                         (SELECT MAX(seller_id)+1 FROM Sellers),
                         false);

\COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.reviews_review_id_seq',
                         (SELECT MAX(review_id)+1 FROM Reviews),
                         false);

\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Inventories FROM 'Inventories.csv' WITH DELIMITER ',' NULL '' CSV

-- \COPY UsersPurchases FROM 'users_purchases.csv' WITH DELIMITER ',' NULL '' CSV

\COPY PurchasesOrders FROM 'purchases_orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY OrdersProducts FROM 'orders_products.csv' WITH DELIMITER ',' NULL '' CSV

\COPY OrdersSellers FROM 'orders_sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY UsersOrders FROM 'users_orders.csv' WITH DELIMITER ',' NULL '' CSV


-- DO NOT DELETE THESE COMMENTS
-- THEY ARE ORIGINAL SKELETON CODE THAT BUILDS
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
-- \COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.users_id_seq',
--                          (SELECT MAX(id)+1 FROM Users),
--                          false);

-- \COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.products_id_seq',
--                          (SELECT MAX(id)+1 FROM Products),
--                          false);

-- \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.purchases_id_seq',
--                          (SELECT MAX(id)+1 FROM Purchases),
--                          false);