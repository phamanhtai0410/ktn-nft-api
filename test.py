from pydash import get

DISCOUNT_DECIMALS = 10 ** 18
d = int(922.64 * DISCOUNT_DECIMALS)
data = {
    'discount': d
}
print(d, get(data, 'discount'), d == get(data, 'discount'))