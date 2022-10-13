-- \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.purchase_id_seq',
--                          (SELECT MAX(id)+1 FROM Purchases),
--                          false);

-- \COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.order_id_seq',
--                          (SELECT MAX(id)+1 FROM Orders),
--                          false);

-- \COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.uid_seq',
--                          (SELECT MAX(id)+1 FROM Users),
--                          false);

-- \COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.product_id_seq',
--                          (SELECT MAX(id)+1 FROM Products),
--                          false);

-- \COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.review_id_seq',
--                          (SELECT MAX(id)+1 FROM Reviews),
--                          false);

-- \COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.seller_id_seq',
--                          (SELECT MAX(id)+1 FROM Sellers),
--                          false);

-- DO NOT DELETE THESE COMMENTS
-- THEY ARE ORIGINAL SKELETON CODE THAT BUILDS
-- \COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- -- since id is auto-generated; we need the next command to adjust the counter
-- -- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);
