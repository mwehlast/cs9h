import sys

def print_banner():
    '''
    Print the program banner. You may change the banner message.
    '''
    # START OF YOUR CODE
    print('''
Welcome to our Python-powered Unit Converter v1.0 by Morten Wehlast Jørgensen!
You can convert Distances, Weights, Volumes to one another, but only
within units of the same category, which are shown below. E.g.: 1 mi in ft

   Distances: ft cm mm mi m yd km in
   Weights: lb mg kg oz g
   Volumes: floz qt cup mL L gal pint
   
   Input must be given as: [QUANTITY] [UNIT FROM] in [UNIT TO]
''')


#Distances = 'd', base unit is metres
#Volumes   = 'v', base unit is liters
#Weights   = 'w', base unit is grams
units = { 'm': ['d', 1],
         'cm': ['d', 0.01],
         'mm': ['d', 0.001],
         'km': ['d', 1000],
         'in': ['d', 0.0254],
         'ft': ['d', 0.3048],
         'yd': ['d', 0.9144],
         'mi': ['d', 1609.34],
          'L': ['v', 1],
         'mL': ['v', 0.001],
       'floz': ['v', 0.0295735],
        'cup': ['v', 0.236588],
       'pint': ['v', 0.473176],
         'qt': ['v', 0.946353],
        'gal': ['v', 3.78541],
          'g': ['w', 1],
         'kg': ['w', 1000],
         'mg': ['w', 0.001],
         'oz': ['w',28.3495],
         'lb': ['w', 453.592]          
        }


def convert(command):
    '''
    Handle a SINGLE user input, which given the command, either print
    the conversion result, or print an error, or exit the program.
    Please follow the requirements listed on project website.
    :param command: User input

    >>> convert('1 m in km')
    1 m = 0.001000 km
    '''
    
    # START OF YOUR CODE
    global units
    if not process_input(command): #Check unput correctness
        return
    
    quantity, unit_from, in_val, unit_to = command.split(' ')
    
    quantity_float = float(quantity)
    to_base_conversion = units[unit_from][1] #Get conversion rate to base unit
    from_base_conversion = units[unit_to][1] #Get conversion rate from base unit
    
    converted_value = quantity_float*to_base_conversion/from_base_conversion
    
    print('{} {} = {:.6f} {}'.format(quantity, unit_from, converted_value, unit_to))
    return
    
    
    # END OF YOUR CODE



# TODO: Add Other Functions Here
def check_domain(unit_to, unit_from):
    """
    Checks whether the units specified exist in same dommain
    >>> check_domain('m','m')
    True
    
    >>> check_domain('m', 'L')
    False
    
    >>> check_domain('alice', 'bob')
    False
    """
    global units
    
    if unit_from not in units or unit_to not in units:
        return False
    
    return units[unit_to][0] == units[unit_from][0]

def process_input(command):
    """
    Splits input string into values needed for calculating conversion
    And checks if input was given in the right way
    Input: command provided by user 
    e.g. '10 m in km'
    Output:  quantity, unit from, unit to
    
    >>> process_input('10 m in km')
    True
    """
    
    global units
    
    if command is None:
        print('Error: Please provide input.')
        return False
    
    if command == 'q':
        print('\n\n Thank you for converting with us! Bye! \n\n')
        sys.exit()
    
    try:
        quantity, unit_from, in_val, unit_to = command.split(' ') #Check if input has all components
    except:
        print('Error: Please provide input as specified.')
        return False
    
    try:
        float(quantity) #Check if quantity is float
    except:
        print('Error: Quantity specified must be a real number.')
        return False
    
    if not check_domain(unit_from, unit_to): #Check domain
        print('Error: Units converted between must be valid and in the same domain.')
        return False
    
    if in_val != 'in': #Check spelling of 'in'
        print('Error: Please provide input as specified.')
        return False
    

    return True


###########################################
# DO NOT MODIFY ANYTHING BELOW
###########################################
    

def get_user_input():
    """
    Print the prompt and wait for user input
    :return: User input
    """
    return input('Convert [AMT SOURCE_UNIT in DEST_UNIT, or (q)uit]: ')


if __name__ == '__main__':
    print_banner()
    while True:
        command = get_user_input()
        convert(command)
