import xmltodict

DATA_PATH = 'program_data.xml'

def upload_program_data():
    file = open(DATA_PATH, 'r')
    xml_data = file.read()
    file.close()
    data = xmltodict.parse(xml_data)
    return data

def get_saved_token():
    data = upload_program_data()
    return data['data']['token']

def get_spent_money():
    data = upload_program_data()
    return data['data']['spent_money']

def update_token(new_token):
    # If u ll open file with 'w', file content will be deleted
    file = open(DATA_PATH, 'r')
    xml_data = file.read()
    file.close()
    file = open(DATA_PATH, 'w')
    data = xmltodict.parse(xml_data)
    data['data']['token'] = new_token
    file.write(xmltodict.unparse(data))
    file.close()

def update_spent_money(amount_of_money):
    file = open(DATA_PATH, 'r')
    xml_data = file.read()
    file.close()
    file = open(DATA_PATH, 'w')
    data = xmltodict.parse(xml_data)
    data['data']['spent_money'] = \
        float(data['data']['spent_money']) + amount_of_money
    file.write(xmltodict.unparse(data))
    file.close()




