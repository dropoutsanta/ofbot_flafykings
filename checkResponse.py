import json

def check_response_type(response):
    
    if 'request' in response:
       
        # Handle the first response type
        return 1

    elif 'role' in response and 'content' in response:
        print("NO FUNCTION CALLED")
        # Handle the second response type
        return 2
    elif 'assistantResponse' in response:
        return 3
    elif 'compliment' in response:
        return 4
    elif 'answerUser' in response: 
        #User Info 
        return 5
    elif 'offer' in response:
        return 6
    elif 'unknown' in response:
        return 7
    else:
        print('Response type is unknown.')
        return 0