from models.user import User
from models.product import Product
import utils


def main():
    user = User("John")
    product = Product("Laptop", 999)
    utils.log("Initializing main function")
    user.purchase_product(product)
    utils.log("Purchase complete")


if __name__ == "__main__":
    main()
