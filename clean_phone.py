# for testing


def clean_phone(matches: list):
    cleaned_matches = [[char for char in match if char.isdigit() or char == '+'] for match in matches]
    phone_numbers = [match for match in cleaned_matches if len(match) >= 9]

    for phone_number in phone_numbers:
        phone_number.insert(-3, ' ')
        phone_number.insert(-7, ' ')
        phone_number.insert(-11, ' ')

    phone_numbers_cleaned = ', '.join(set([''.join(phone_number).strip() for phone_number in phone_numbers]))
    return phone_numbers_cleaned


print(clean_phone(['.10.2018', ' 602504586', '602504586']))
print(clean_phone([' 777.69.52.69']))
print(clean_phone([' 722091723']))
print(clean_phone(['00420-603 179 292']))
print(clean_phone(['603 179 292']))
print(clean_phone(['+35 603 179 292', '223081', ' 25.11.201']))

