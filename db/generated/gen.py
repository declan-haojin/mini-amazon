from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from collections import OrderedDict

num_users = 100
num_products = 100
num_reviews = 50
num_sellers = 100
num_orders = 100
num_history = num_users

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('../data/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = f'{str(fake.random_int(max=500000))}'
            writer.writerow([uid, email, password, firstname, lastname, balance])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('../data/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('../data/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_orders(num_orders):
    with open('../data/Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for oid in range(num_orders):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            purchase_id = fake.unique.random_int(min=0, max=num_orders-1)
            n_items = fake.random_int(min=0, max=20)
            amount = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            status = fake.random_elements(elements=OrderedDict([
                ("Confirmed", 0.3),
                ("Processing", 0.2),
                ("Out for Delivery", 0.2),
                ("Delivered", 0.3),
                ]), unique=False
            )
            pid = fake.random_element(elements=available_pids)
            writer.writerow([uid,purchase_id,n_items,amount,status,pid])
        print(f'{num_orders} generated')
    return

def gen_reviews(num_reviews):
    with open('../data/Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for review_id in range(num_reviews):
            if review_id % 10 == 0:
                print(f'{review_id}', end=' ', flush=True)
            uid = fake.unique.random_int(min=0, max=num_users-1)
            sid = fake.unique.random_int(min=0, max=num_sellers-1)
            pid = fake.unique.random_int(min=0, max=num_products-1)
            rating = fake.random_digit()
            review_time = fake.date_time()
            content = fake.sentence(nb_words=4)[:-1]
            writer.writerow([review_id, review_time, uid, sid, pid, content, rating])
        print(f'{num_reviews} generated')
    return

# def gen_seller_reviews(num_seller_reviews):
#     _gen_reviews(num_seller_reviews)
#     return

# def gen_product_reviews(num_product_reviews):
#     _gen_reviews(num_product_reviews)
#     return

def gen_sellers(num_sellers):
    with open('../data/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for sid in range(num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{sid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = f'{str(fake.random_int(max=500000))}'
            writer.writerow([sid, email, password, firstname, lastname, balance])
        print(f'{num_sellers} generated')
    return

def gen_cart(num_users):
    with open('../data/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            n_items = fake.random_int(min=0, max=20) #Any buyer can have at most 20 types of items in his/her cart.
            for n in range (0,n_items-1):
                fake.random_elements(elements=available_pids, unique=True)
                qty = f'{str(fake.random_int(max=40))}'
                price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
                pid = fake.unique.random_int(min=0, max=num_products-1)
                writer.writerow([uid, pid, qty, price])
        print(f'{num_users} generated')
    return

def gen_inventories(num_sellers):
    with open('../data/Inventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...', end=' ', flush=True)
        for sid in range (num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            n_items = fake.random_int(min=0, max=20) #Any seller can have at most 20 types of items in his/her inventory.
            for n in range (0,n_items-1):
                fake.random_elements(elements=available_pids, unique=True) #.unique to ensure no repeated products for each seller.
                qty = f'{str(fake.random_int(max=40))}' #At most 40 quantity of any item.
                pid = fake.unique.random_int(min=0, max=num_products-1)
                writer.writerow([sid, pid, qty])
        print(f'{num_sellers} generated')
    return

# Generate data for relationship table

def gen_users_purchases(num_pairs):
    with open('../data/users_purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users_purchases_pair...', end=' ', flush=True)
        for n in range (num_pairs):
            uid = fake.random_int(min=0, max=num_users-1)
            purchase_id = fake.unique.random_int(min=0, max=num_orders-1)
            writer.writerow([uid, purchase_id])
        print(f'{num_pairs} generated')
    return

def gen_purchases_orders(num_pairs):
    with open('../data/purchases_orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases_orders_pair...', end=' ', flush=True)
        for n in range (num_pairs):
            purchase_id = fake.random_int(min=0, max=num_history-1)
            order_id = fake.unique.random_int(min=0, max=num_orders-1)
            writer.writerow([purchase_id,order_id])
        print(f'{num_pairs} generated')
    return

def gen_orders_products(num_pairs):
    with open('../data/orders_products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders_products_pair...', end=' ', flush=True)
        for n in range (num_pairs):
            order_id = fake.random_int(min=0, max=num_orders-1)
            pid = fake.random_element(elements=available_pids)
            writer.writerow([order_id,pid])
        print(f'{num_pairs} generated')
    return

def gen_orders_sellers(num_orders):
    with open('../data/orders_sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders_sellers_pair...', end=' ', flush=True)
        for n in range (num_pairs):
            order_id = fake.unique.random_int(min=0, max=num_orders-1)
            sid = fake.random_int(min=0, max=num_sellers-1)
            writer.writerow([order_id,sid])
        print(f'{num_orders} generated')
    return

def gen_users_orders(num_pairs):
    with open('../data/users_orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users_orders_pair...', end=' ', flush=True)
        for n in range (num_pairs):
            uid = fake.random_int(min=0, max=num_users-1)
            order_id = fake.unique.random_int(min=0, max=num_pairs-1)
            writer.writerow([uid,order_id])
        print(f'{num_pairs} generated')
    return

# gen_users(num_users)
available_pids = gen_products(num_products)
assert num_orders <= len(available_pids)
gen_purchases(num_orders, available_pids)
gen_sellers(num_sellers)
gen_products(num_products)
gen_orders(num_orders)
gen_reviews(num_reviews)
gen_cart(num_users)
gen_inventories(num_sellers)
gen_users_purchases(num_orders)
gen_purchases_orders(num_history)
gen_orders_products(num_orders)
gen_orders_sellers(num_orders)
gen_users_orders(num_orders)

# gen_seller_reviews(num_reviews)
# gen_product_reviews(num_reviews)
