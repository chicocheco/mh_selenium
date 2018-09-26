def create_url(json_response):

    # projects with their own base url: https://www.sreality.cz/projekt-detail
    try:
        project_base = 'https://www.sreality.cz/projekt-detail'
        project_name = json_response['seo'].lower()
        project_id = json_response['_embedded']['estates']['filter']['project']
        return f'{project_base}/{project_name}/{project_id}'

    # estates with their own base url: https://www.sreality.cz/detail
    except AttributeError:
        base = 'https://www.sreality.cz/detail'
        locality = json_response['seo']['locality']
        id_offer = json_response['_links']['self']['href'].split('/')[-1]
        title1 = json_response['name']['value']

        lst = title1.split()
        new_lst = []

        # types (from &category_type_cb=1 to &category_type_cb=3)
        if lst[0] == 'Prodej':
            new_lst.insert(0, '/prodej')
        elif lst[0] == 'Pronájem':
            new_lst.insert(0, '/pronajem')
        elif lst[0] == 'Dražba':
            new_lst.insert(0, '/drazby')

        # main types (flats: &category_main_cb=1, houses and their subtypes: &category_main_cb=2&category_sub_cb=
        # {'Rodinný': '37', 'Vila': '39', 'Chalupa': '43', 'Chata': '33', 'Na klíč': '40',
        # 'Zemědělská usedlost': '44', 'Památka/jiné': '35'})
        if lst[1] == 'bytu':
            new_lst.insert(1, '/byt')

        elif lst[1:3] == ['rodinného', 'domu']:
            new_lst.insert(1, '/dum/rodinny')
        elif lst[1] == 'vily':
            new_lst.insert(1, '/dum/vila')
        elif lst[1] == 'chalupy':
            new_lst.insert(1, '/dum/chalupa')
        elif lst[1] == 'chaty':
            new_lst.insert(1, '/dum/chata')
        elif lst[1:4] == ['projektu', 'na', 'klíč']:
            new_lst.insert(1, '/dum/na-klic')
        elif lst[1:3] == ['zemědělské', 'usedlosti']:
            new_lst.insert(1, '/dum/zemedelska-usedlost')
        elif lst[1] == 'památky':
            new_lst.insert(1, '/dum/pamatka')

        # main type (grounds: &category_main_cb=3 and their subtypes: &category_main_cb=2&category_sub_cb=...)
        elif lst[1:3] == ['stavebního', 'pozemku']:
            new_lst.insert(1, '/pozemek/bydleni')
        elif lst[1:3] == ['komerčního', 'pozemku']:
            new_lst.insert(1, '/pozemek/komercni')
        elif lst[1] == 'pole':
            new_lst.insert(1, '/pozemek/pole')
        elif lst[1] == 'louky':
            new_lst.insert(1, '/pozemek/louka')
        elif lst[1] == 'lesa':
            new_lst.insert(1, '/pozemek/les')
        elif lst[1:4] == ['rybníku', '(vodní', 'plochy)']:
            new_lst.insert(1, '/pozemek/rybnik')
        elif lst[1:3] == ['sadu,', 'vinice']:
            new_lst.insert(1, '/pozemek/sady-vinice')
        elif lst[1] == 'zahrady':
            new_lst.insert(1, '/pozemek/zahrada')
        elif lst[1] == 'pozemku':
            new_lst.insert(1, '/pozemek/ostatni-pozemky')

        # main type (grounds: &category_main_cb=4 and their subtypes: &category_main_cb=2&category_sub_cb=...)
        # {'Kanceláře': '25', 'Sklady': '26', 'Výroba': '27', 'Obchodní prostory': '28', 'Ubytování': '29',
        # 'Restaurace': '30', 'Zemědělský': '31', 'Činžovní dům': '38', 'Ostatní': '32', 'Virtuální kancelář': '49'}
        if lst[1] == 'kanceláře':
            new_lst.insert(1, '/komercni/kancelare')
        elif lst[1:3] == ['skladového', 'prostoru']:
            new_lst.insert(1, '/komercni/sklad')
        elif lst[1:4] == ['výrobní', 'haly,', 'prostoru']:
            new_lst.insert(1, '/komercni/vyrobni-prostor')
        elif lst[1:3] == ['obchodního', 'prostoru']:
            new_lst.insert(1, '/komercni/obchodni-prostor')
        elif lst[1:3] == ['ubytovacího', 'zařízení']:
            new_lst.insert(1, '/komercni/ubytovani')
        elif lst[1] == 'restaurace':
            new_lst.insert(1, '/komercni/restaurace')
        elif lst[1:3] == ['zemědělského', 'objektu']:
            new_lst.insert(1, '/komercni/zemedelsky')
        elif lst[1:3] == ['činžovního', 'domu']:
            new_lst.insert(1, '/komercni/cinzovni-dum')
        elif lst[1:3] == ['komerční', 'nemovitosti']:
            new_lst.insert(1, '/komercni/ostatni-komercni-prostory')

        # main type (others: &category_main_cb=5 and their subtypes: &category_main_cb=2&category_sub_cb=...)
        elif lst[1] == 'garáže':
            new_lst.insert(1, '/ostatni/garaz')
        elif lst[1:3] == ['garážového', 'stání']:
            new_lst.insert(1, '/ostatni/garazove-stani')
        elif lst[1:3] == ['mobilheimu,', 'mobilního']:
            new_lst.insert(1, '/ostatni/mobilni-domek')
        elif lst[1:3] == ['vinného', 'sklepa']:
            new_lst.insert(1, '/ostatni/vinny-sklep')
        elif lst[1:3] == ['půdního', 'prostoru']:
            new_lst.insert(1, '/ostatni/pudni-prostor')
        elif lst[1:4] == ['specifického', 'typu', 'nemovitosti']:
            new_lst.insert(1, '/ostatni/jine-nemovitosti')

        # subtypes of flats (from "&category_sub_cb=2" to "&category_sub_cb=12")
        rooms = ['1+kk', '1+1', '2+kk', '2+1', '3+kk', '3+1', '4+kk', '4+1', '5+kk', '5+1']
        if lst[2] in rooms:
            new_lst.insert(2, '/' + lst[2])
        elif lst[2] == 'atypické':
            new_lst.insert(2, '/atypicky')
        elif lst[2:6] == ['6', 'pokojů', 'a', 'více']:
            new_lst.insert(2, '/6-a-vice')

        new_lst_joined = ''.join(new_lst)

        # TODO: check if the link works

        return f'{base}{new_lst_joined}/{locality}/{id_offer}'
