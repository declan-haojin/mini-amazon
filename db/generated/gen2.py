from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from collections import OrderedDict
import random
import numpy as np
from IPython import embed

num_users = 500
num_products = 1000
num_sellers = 1000

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

# generate unique uid-purchase_id mapping
uid_ls = np.arange(0, num_users).tolist()
purchase_ls = np.arange(0, num_users).tolist()
random.shuffle(purchase_ls)
num_orders = []
for i in range(num_users):
    num_orders.append(fake.random_int(max=10))
total_order = sum(num_orders)

# embed()
def _flatten(l):
    return [item for sublist in l for item in sublist]

Faker.seed(1)
fake_oid = Faker()

oid_big_ls = []
oid2uid = {}
oid2status = {}
oid2amt = {}

unique_random_oid = np.arange(total_order).tolist()
random.shuffle(unique_random_oid)
# embed()

idx = 0 
for uid in range(num_users):
    oid_ls = []
    for j in range(num_orders[uid]):
        # oid = fake_oid.unique.random_int(min=0, max=total_order-1)
        oid = unique_random_oid[idx]
        oid_ls.append(oid)
        oid2uid[oid] = uid
        status = fake.random_elements(elements=OrderedDict([
        ("Fulfilled", 0.5),
        ("Processing", 0.5)]), unique=False)[0]
        amount = fake.random_int(max=10000)
        oid2status[oid] = status
        oid2amt[oid] = amount
        idx += 1
    oid_big_ls.append(oid_ls)


oid_ele = _flatten(oid_big_ls)

seller_product_pair = []
with open('../data/Inventories.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        res = row[0].split(',')
        seller_product_pair.append([res[0], res[1].strip(' "" ')])

sp_pair_sample = random.sample(seller_product_pair, total_order)
oid2sp_pair = dict(zip(oid_ele, sp_pair_sample))

def gen_orders(total_order):
    with open('../data/Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for oid in oid_ele:
            update_at = fake.date_time()
            uid = oid2uid[oid]
            purchase_id = purchase_ls[uid]
            num_items = fake.random_int(max=10)
            amount = oid2amt[oid]
            status = oid2status[oid]
            seller_id = int(oid2sp_pair[oid][0])
            product_id = int(oid2sp_pair[oid][1])
            writer.writerow([uid, purchase_id, oid, num_items, amount, status, product_id, seller_id, update_at])
    return

uid2tot_amt = {}
uid2all_status = {}
for uid in range(num_users):
    total_amt = []
    status_ls = []
    oid_ls = oid_big_ls[uid]
    for oid in oid_ls:
        total_amt.append(oid2amt[oid])
        status_ls.append(oid2status[oid])
    uid2tot_amt[uid] = sum(total_amt)
    uid2all_status[uid] = status_ls

purchase_id2status = {}
for uid in range(num_users):
    purchase_id = purchase_ls[uid]
    all_status = uid2all_status[uid]
    if len(set(all_status)) == 1 and set(all_status) == "Fulfilled":
        purchase_id2status[purchase_id] = "Fulfilled"
    else:
        purchase_id2status[purchase_id] = "Processing"



def gen_purchases(num_users):
    with open('../data/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for uid in range(num_users):
            purchase_id = purchase_ls[uid]
            oid_ls = oid_big_ls[uid]
            num_orders = len(oid_ls)
            total_amount = uid2tot_amt[uid]
            status = purchase_id2status[purchase_id]
            time_purchased = fake.date_time()
            writer.writerow([uid, purchase_id, num_orders, total_amount, status, time_purchased])
    return


num_pairs = 300
review_sp_pair_sample_idx = random.sample(oid_ele, num_pairs)
review_sp_pair_sample = []

rid2usp_dup = {}
for rid, oid in enumerate(review_sp_pair_sample_idx):
    review_sp_pair_sample.append(oid2sp_pair[oid])
    uid = oid2uid[oid]
    rid2usp_dup[rid] = (uid, int(review_sp_pair_sample[rid][0]), int(review_sp_pair_sample[rid][1]))

rid2usp_set = set(list(rid2usp_dup.values()))
num_reviews = len(rid2usp_set)

rid2usp = dict(zip(range(num_reviews), rid2usp_set))

# embed()


def gen_reviews(num_reviews):
    with open('../data/Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for rid in range(num_reviews):
            uid = rid2usp[rid][0]
            sid = rid2usp[rid][1]
            pid = rid2usp[rid][2]
            purchase_id = purchase_ls[uid]
            content = fake.sentence(nb_words=4)[:-1]
            review_type = fake.random_element(elements=('seller', 'product'))
            review_time = fake.date_time()
            rating = fake.random_digit()
            vote = fake.random_digit()
            writer.writerow([uid, rid, content, rating, review_time, sid, pid, review_type, vote])
    return


available_pids = []
for pid in range(num_products):
    available = 'true'
    if available == 'true':
        available_pids.append(pid)

def gen_cart(num_users):
    key = set()
    pid = -1
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
                pid_ori = fake.random_int(min=0, max=num_products-1)
                while (uid, pid_ori) in key:
                        pid_ori = fake.random_int(min=0, max=num_products-1)
                key.add((uid, pid_ori))
                pid = pid_ori
                sid = fake.random_int(min=0, max=num_sellers-1)
                writer.writerow([uid, sid, pid, qty])
        print(f'{num_users} generated')
    return

gen_orders(total_order)
gen_purchases(num_users)
gen_reviews(num_reviews)
gen_cart(num_users)
