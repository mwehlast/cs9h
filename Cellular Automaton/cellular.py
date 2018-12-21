import argparse
import doctest


def decimal_to_binary(x):
    """
    This function converts a decimal number N into a binary number with 8 bits.
    :param x: The decimal number

    >>> decimal_to_binary(30)
    '00011110'
    >>> decimal_to_binary(139)
    '10001011'
    """
    assert 0 <= x <= 255, "Number should be between 0 and 255"
    
    return '{0:08b}'.format(x)


def generate(rule, steps):
    """
    Generate the image from given rule number and steps
    and print it to the console.
    The output image should have width of 2 * STEPS + 1 and height of STEPS + 1.

    :param rule: The rule number
    :param steps: Number of lines

    >>> generate(30, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 1 1 1 0 0 0 0
    0 0 0 1 1 0 0 1 0 0 0
    0 0 1 1 0 1 1 1 1 0 0
    0 1 1 0 0 1 0 0 0 1 0
    1 1 0 1 1 1 1 0 1 1 1
    
    >>> generate(129, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    1 1 1 1 0 0 0 1 1 1 1
    0 1 1 0 0 1 0 0 1 1 0
    0 0 0 0 0 0 0 0 0 0 0
    1 1 1 1 1 1 1 1 1 1 1
    0 1 1 1 1 1 1 1 1 1 0
    
    >>> generate(44, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 0 1 0 0 0 0 0
    
    >>> generate(233, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    1 1 1 1 0 0 0 1 1 1 1
    1 1 1 1 0 1 0 1 1 1 1
    1 1 1 1 1 0 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1 1
    
    >>> generate(127, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    1 1 1 1 1 1 1 1 1 1 1
    1 0 0 0 0 0 0 0 0 0 1
    1 1 1 1 1 1 1 1 1 1 1
    1 0 0 0 0 0 0 0 0 0 1
    1 1 1 1 1 1 1 1 1 1 1
    """
    
    #Dimensions of image
    n_rows = steps + 1
    n_cols = 2*steps + 1
    
    print('P1 {} {}'.format(n_cols, n_rows)) #Print program number and dimensions
    
    rules_dict = make_rule_dict(rule) #Create dictionary of rules
    row_current = '0'*steps + '1' + '0'*steps #Create initial row
    
    for i in range(0, n_rows): #Iterate over rows 
        
        print(' '.join(row_current)) #Print current row separated by whitespace
        row_new = '' #Initialize new row
        
        for j in range(0, n_cols): #Iterate over columns 
            
            if j == 0: #First index special case
                row_new = row_new + str(rules_dict['0' + row_current[0:2]])
                
            elif j == 2*steps: #Last index special case
                row_new = row_new + str(rules_dict[row_current[j-1:j+1] + '0'])
                
            else: 
                row_new = row_new + str(rules_dict[row_current[j-1:j+2]])

        row_current = row_new #Update new current to newly created

    return

    # END OF YOUR CODE


# TODO: You may add any additional functions here
def make_rule_dict(rule):
    """
    Create a dictionary of rules to update next line in the automaton by lookup
    by current index and its 2 neighbours.
    
    Input: rule number
    Output: a dictionary. 
    """
    rule_dict = {}
    
    #Convert values to binary and assign bitswitch rule to each
    for i in range(0,8):
        rule_dict['{0:03b}'.format(i)] = rule & 2**i #Format rule to scheme for number i
    
    for key, value in rule_dict.items(): #Change to boolean values
        if value > 0:
            rule_dict[key] = 1
        
    return rule_dict


if __name__ == '__main__':
    # START OF YOUR CODE
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Project 1: Cellular Automaton')
    parser.add_argument('rule', help='The Rule', type=int)
    parser.add_argument('steps', help='Number of Steps', type=int)
    args = parser.parse_args()
    rule, steps = args.rule, args.steps

    # END OF YOUR CODE

    assert 0 <= rule <= 255 and steps >= 0
    generate(rule, steps)
