

def create_url(json_response: dict) -> str:
    """Build an URL of an ad based on the data found in the API data of and ad.

    :param json_response: API of a single ad in a dictionary data type.
    :return: Complete URL as a string.
    """

    # projects have a different URL
    try:
        project_base = 'https://www.sreality.cz/projekt-detail'
        project_name = json_response['seo'].lower()
        project_id = json_response['_embedded']['estates']['filter']['project']
        return f'{project_base}/{project_name}/{project_id}'

    except AttributeError:
        base = 'https://www.sreality.cz/detail'
        locality = json_response['seo']['locality']
        id_offer = json_response['_links']['self']['href'].split('/')[-1]
        title = json_response['name']['value']

        title_list = title.split()
        desc = []

        types = {'Prodej': '/prodej', 'Pronájem': '/pronajem', 'Dražba': '/drazby'}
        desc.insert(0, types.get(title_list[0], 'not-found'))

        # special case for flats
        if title_list[1] == 'bytu':
            if title_list[2] == 'atypické':
                desc.insert(1, '/byt/atypicky')
            elif title_list[2] == '6':
                desc.insert(1, '/byt/6-a-vice')
            else:
                desc.insert(1, f'/byt/{title_list[2]}')

        else:
            sub_types = {'rodinného': '/dum/rodinny', 'vily': '/dum/vila', 'chalupy': '/dum/chalupa',
                         'chaty': '/dum/chata',
                         'projektu': '/dum/na-klic', 'zemědělské': '/dum/zemedelska-usedlost',
                         'památky': '/dum/pamatka',
                         'stavebního': '/pozemek/bydleni', 'komerčního': '/pozemek/komercni', 'pole': '/pozemek/pole',
                         'louky': '/pozemek/pole', 'lesa': '/pozemek/les', 'rybníku': '/pozemek/rybnik',
                         'sadu': '/pozemek/sady-vinice', 'zahrady': '/pozemek/zahrada',
                         'pozemku': '/pozemek/ostatni-pozemky',
                         'kanceláře': '/komercni/kancelare', 'skladového': '/komercni/sklad',
                         'výrobní': '/komercni/vyrobni-prostor', 'obchodního': '/komercni/obchodni-prostor',
                         'ubytovacího': '/komercni/ubytovani', 'restaurace': '/komercni/restaurace',
                         'zemědělského': '/komercni/zemedelsky', 'činžovního': '/komercni/cinzovni-dum',
                         'komerční': '/komercni/ostatni-komercni-prostory', 'garáže': '/ostatni/garaz',
                         'garážového': '/ostatni/garazove-stani', 'mobilheimu,': '/ostatni/mobilni-domek',
                         'vinného': '/ostatni/vinny-sklep', 'půdního': '/ostatni/pudni-prostor',
                         'specifického': '/ostatni/jine-nemovitosti'}

            desc.insert(1, sub_types.get(title_list[1], 'not-found'))

        desc_string = ''.join(desc)

        return f'{base}{desc_string}/{locality}/{id_offer}'
