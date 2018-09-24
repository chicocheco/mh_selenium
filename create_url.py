
# only for testing
def create_url(json_response):
    base = 'https://www.sreality.cz/detail'
    locality = '/' + json_response['seo']['locality']
    id_offer = '/' + json_response['_links']['self']['href'].split('/')[-1]
    title1 = json_response['name']['value']

    lst = title1.split()
    new_lst = []

    if lst[0] == 'Prodej':
        new_lst.insert(0, '/prodej')
    elif lst[0] == 'Pron\u00e1jem':
        new_lst.insert(0, '/pronajem')
    elif lst[0] == 'Dra\u017eba':
        new_lst.insert(0, '/drazby')

    if lst[1] == 'bytu':
        new_lst.insert(1, '/byt')
    elif lst[1] == 'rodinn\u00e9ho':
        new_lst.insert(2, '/rodinny')
    elif lst[1] == 'vily':
        new_lst.insert(2, '/vila')
        new_lst.insert(1, '/dum')
    elif lst[1] == 'chaty':
        new_lst.insert(1, '/dum/chata')
    elif lst[1] == 'chalupy':
        new_lst.insert(1, '/dum/chalupa')
    elif lst[1:4] == ['projektu', 'na', 'klíč']:
        new_lst.insert(1, '/dum/na-klic')
    elif lst[1:3] == ['zemědělské', 'usedlosti']:
        new_lst.insert(1, '/dum/zemedelska-usedlost')

    if lst[2] == 'domu':
        new_lst.insert(1, '/dum')
    elif lst[2] == 'atypick\u00e9':
        new_lst.insert(2, '/atypicky')
    elif lst[2] == '6 pokoj\u016f a v\u00edce':
        new_lst.insert(2, '/6-a-vice')

    rooms = ['1+kk', '1+1', '2+kk', '2+1', '3+kk', '3+1', '4+kk', '4+1', '5+kk', '5+1']
    if lst[2] in rooms:
        new_lst.insert(2, '/' + lst[2])

    new_lst_joined = ''.join(new_lst)

    return print(f'{base}{new_lst_joined}{locality}{id_offer}')


# with open('/home/standa/PycharmProjects/mh/testovaci.json') as response:
#     create_url(response)

