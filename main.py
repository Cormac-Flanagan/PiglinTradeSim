import logging
import concurrent.futures
import random
from matplotlib import pyplot as plt
import tqdm
import gc

# Amount of trade simulations done (Higher = Slower)
experiments = 1000000000
# Amount of Simulations done at once (Higher = Faster, More resource intense)
workers = 10000
# Amount of Pearls each trader is required to get
requiredPearls = 16


pbar = tqdm.tqdm(total=experiments)


class piglinTrade:
    def __init__(self):
        self.value = {}

    def update(self, name):
        # Simulated Trade
        pbar.update(1)
        ePearl = 0
        gold = 0
        while ePearl < requiredPearls:
            # Simulated Trading
            gold += 1
            value = random.randint(0, 459)
            if value <= 10:
                ePearl += random.randint(2,4)
        local_copy = self.value
        if gold in local_copy:
            local_copy[gold] += 1
        else:
            local_copy[gold] = 1
        self.value = local_copy
        gc.collect()




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    database = piglinTrade()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for index in range(experiments):
            executor.submit(database.update, index)
    logging.info(f"Testing update. Ending value is {database.value}")

    keys = list(database.value)
    keys.sort()
    print(keys)
    amount = []
    for i in keys:
        amount.append(database.value[i])


    plt.bar(keys, amount, align='center', alpha=0.5)
    plt.ylabel('Times Achieved')
    plt.xlabel("gold required")
    plt.suptitle(f'Average gold required for {requiredPearls}')
    plt.title(f"tested with {experiments} experiments")
    pbar.close()
    plt.show()
