_pd = 1
_i = [{
    "p": 45,
    "d": 1
},
    {
        "p": 65,
        "d": 4.5
    }
    ,
    {
        "p": 165,
        "d": 3.5
    }
]


def ge(item):
    p = item.get('p') * (_pd / 100)
    d = (item.get('p') - p) * (item.get('d') / 100)

    return p + d

print(sum(ge(x) for x in _i))
