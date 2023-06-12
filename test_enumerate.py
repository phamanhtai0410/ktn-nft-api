import web3

x = 0.01
_x = web3.Web3.toWei(x, 'ether')
print(_x)
print((web3.Web3.toWei(0.24, 'ether') - _x) / 10 ** 18)




a = [1, 2, 3]
for (_idx, _item) in enumerate(a):
    print(_idx, _item)
    
