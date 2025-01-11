from faker import Faker
faker = Faker()

def get_faker_data():
    """
        Please modify the content of this tags and map it accordingly based on your requirements
    """
    # tags = {
    #     'price': faker.first_name(),
    #     'name' : faker.first_name(),
    #     'title' : faker.first_name(),
    #     'author' : faker.first_name(),
    # }

    tags = {
        'Applicant_ID': faker.first_name(),
        'First_Name' : faker.first_name(),
        'Last_Name' : faker.first_name(),
        'Address_Line_Data' : faker.address(),
        'Municipality' : faker.first_name(),
        'Postal_Code' : faker.postalcode(),
    }
    
    return tags
