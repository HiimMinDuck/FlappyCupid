#mo=moveObject
#so=stayObject
#x,y is position of object

def checkHitBox(mo_x, mo_y, mo_width, mo_height, so_x, so_y, so_width, so_height):
    if(mo_x + mo_width > so_x) and (mo_x < so_x + so_width) and (mo_y + mo_height > so_y) and (mo_y < so_y + so_height):
        #if mo want to hit the stay object on the x-axis so x and width index of mo and stay object must be like: 
        # so_x < mo_x <  mo_x+mo_width < so_x+so_width
        #same with y-axis, we have
        # so_y < mo_y < mo_y+mo_height < mo_y+mo_height
        return True

#if u dont understand, u should imagine that u have 2 line:
    #line 1 start at 1 and end at 5 (line 1 like the stay object)
        #start is like so_x and end is like so_x+so_width
    #if the line 2 want hit the line 1, so line 2 need start in 2 case:
        #case 1: start lower than 1, but end bigger 1 (mo_x < so_x and mo_x+mo_width > so_x)
        #case 2: start betwen than 1 and 5 and end bigger than 1 (mo_x>so_x and mo_x < so_x+so_width)
#in all case the first logic is opposite (mo_x < so_x and mo_x > so_x)
#so i take the second logic mo_x+mo_width > so_x and mo_x < so_x+so_width

#sorry, because my english is so bad :< 