# How to setup
   
    git clone git@ghe.megaleo.com:perfscale/appscale.git
    python3 -m venv venv
    source venv/bin/activate
    cd appscale/parser
    pip3 install --upgrade pip
    pip3 install -r requirements.txt


# How to run the program
    
    python3 parse.py

    usage: python3 parser.py [-h] [-t TEMPLATE] [-o OUTPUT] [-r REPEAT]

    Feed this file with the template location, tags to be modified and how many times the template to be repeated

    options:
    -h, --help            show this help message and exit
    -t TEMPLATE, --template TEMPLATE
                            template location to process, e.g template/Put_Applicant_001_of_001.xml
    -o OUTPUT, --output OUTPUT
                            output location for the processed fule, e.g output/Output.xml
    -r REPEAT, --repeat REPEAT
                            repetition of the template, e.g 20
    
## Links
   - [Git Repository](https://ghe.megaleo.com/perfscale/appscale.git)
   - [How to use the library](https://confluence.workday.com/display/~vinod.krishnan/XML+Parser)