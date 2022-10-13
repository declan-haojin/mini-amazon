from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_reviews = 10
num_sellers = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
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
    with open('Products.csv', 'w') as f:
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
    with open('Purchases.csv', 'w') as f:
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
    # TO-DO
    return

def _gen_reviews(num_reviews):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for review_id in range(num_reviews):
            if review_id % 10 == 0:
                print(f'{review_id}', end=' ', flush=True)
            content = fake.sentence(nb_words=4)[:-1]
            writer.writerow([review_id, content])
        print(f'{num_reviews} generated')
    return

def gen_seller_reviews(num_seller_reviews):
    _gen_reviews(num_seller_reviews)
    return

def gen_product_reviews(num_product_reviews):
    _gen_reviews(num_product_reviews)
    return

def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
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

def gen_cart(num_carts):
    #TO-DO
    return

def gen_inventories(num_sellers):
    with open('Inventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...', end=' ', flush=True)
        for sid in range (num_sellers):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            n_items = fake.random_int(min=0, max=20) #Any seller can have at most 20 types of items in his/her inventory.
            for n in range (0,n_items-1):
                pid = fake.unique.random_int(min=0, max=num_products-1) #.unique to ensure no repeated products for each seller.
                qty = f'{str(fake.random_int(max=40))}' #At most 40 quantity of any item.
                writer.writerow([sid, pid, qty])
        print(f'{num_sellers} generated')
    return

# Generate data for relationship table

def gen_users_purchases(num_pairs):
    #TO-DO
    return

def gen_purchases_orders(num_pairs):
    #TO-DO
    return

def gen_orders_products(num_pairs):
    #TO-DO
    return

def gen_orders_sellers(num_pairs):
    #TO-DO
    return

def gen_users_orders(num_pairs):
    #TO-DO
    return

gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_seller_reviews(num_reviews)
gen_product_reviews(num_reviews)
gen_sellers(num_sellers)
