from util import MockObject

mock = MockObject()

def get_mock_data():
    """
        Please modify the content of this tags and map it accordingly based on your requirements
    """
    # tags = {
    #     'price': mock.price(),
    #     'name' : mock.name(),
    #     'title' : mock.title(),
    #     'author' : mock.author(),
    # }

    tags = {
        'Applicant_ID': mock.application_id(),
        'First_Name' : mock.last_name(),
        'Last_Name' : mock.first_name(),
        'Address_Line_Data' : mock.address(),
        'Municipality' : mock.municipality(['Kings','Clarks','Powel','Sworn','Brown','Yale','Madison','Drake']),
        'Postal_Code' : mock.postalcode(),
    }
    
    return tags
