def init():
    return [['-','-','-'],['-','-','-'],['-','-','-']]

def show(b):
    x = []
    for i in b:
        x.append(''.join(i))
    for j in x:
        strings = '\n'.join(x)
    return strings+'\n'
    
def movex(b,i,j):
    i -= 1
    j -= 1
    b[i][j] = 'x'
        
def moveo(b,i,j):
    i -= 1
    j -= 1
    b[i][j] = 'o'
    
def countmoves(b):
    move_count=0
    for i in b:
        for j in i:
            if j != '-':
                move_count += 1
    return move_count

def getmoves(b):
    x_movelist = []
    o_movelist = []
    move_dict = {'x':x_movelist, 'o':o_movelist}

    for u,i in enumerate(b):
        for v,j in enumerate(i):
            if j == 'x':
                x_move = (u+1,v+1)
                x_movelist.append(x_move)
            elif j == 'o':
                o_move = (u+1,v+1)
                o_movelist.append(o_move)
            
    move_dict['x'] = x_movelist
    move_dict['o'] = o_movelist

    return move_dict

def winsx(b):
    streak_counter_i = 0
    streak_counter_j = 0
    streak_counter_d = 0
    dict_moves = getmoves(b)
    list_moves = dict_moves['x']


    # For a horizontal win
    
    horizontal_list = []
    for coord_tuple_i in list_moves:
        horizontal_list.append(coord_tuple_i[0])
    
    m_h = max([horizontal_list.count(a) for a in horizontal_list])
    mode_h = [x for x in horizontal_list if horizontal_list.count(x) == m_h][0] if m_h>1 else None
    
    control_i = mode_h
    for coord_tuple_i in list_moves:
        if coord_tuple_i[0] == control_i:
            streak_counter_i += 1
    
    # For a vertical win
    
    vertical_list = []
    for coord_tuple_i in list_moves:
        vertical_list.append(coord_tuple_i[1])
    
    m_v = max([vertical_list.count(a) for a in vertical_list])
    mode_v = [x for x in vertical_list if vertical_list.count(x) == m_v][0] if m_v>1 else None
            
    control_j = mode_v
    for coord_tuple_j in list_moves:
        if coord_tuple_j[1] == control_j:
            streak_counter_j += 1
            
    # For a diagonal win - Both cases
    if b[0][2] == 'x':
        if b[1][1] == 'x':
            if b[2][0] == 'x':
                streak_counter_d = 3

    if b[0][0] == 'x':
        if b[1][1] == 'x':
            if b[2][2] == 'x':
                streak_counter_d = 3
                    
    if streak_counter_i == 3:
        return True
    elif streak_counter_j == 3:
        return True
    elif streak_counter_d == 3:
        return True
    else:
        return False
            
def winso(b):
    streak_counter_i = 0
    streak_counter_j = 0
    streak_counter_d = 0
    dict_moves = getmoves(b)
    list_moves = dict_moves['o']


    # For a horizontal win
    
    horizontal_list = []
    for coord_tuple_i in list_moves:
        horizontal_list.append(coord_tuple_i[0])
    
    m_h = max([horizontal_list.count(a) for a in horizontal_list])
    mode_h = [x for x in horizontal_list if horizontal_list.count(x) == m_h][0] if m_h>1 else None
    
    control_i = mode_h
    for coord_tuple_i in list_moves:
        if coord_tuple_i[0] == control_i:
            streak_counter_i += 1
    
    # For a vertical win
    
    vertical_list = []
    for coord_tuple_i in list_moves:
        vertical_list.append(coord_tuple_i[1])
    
    m_v = max([vertical_list.count(a) for a in vertical_list])
    mode_v = [x for x in vertical_list if vertical_list.count(x) == m_v][0] if m_v>1 else None
            
    control_j = mode_v
    for coord_tuple_j in list_moves:
        if coord_tuple_j[1] == control_j:
            streak_counter_j += 1
            
    # For a diagonal win - Both cases
    if b[0][2] == 'o':
        if b[1][1] == 'o':
            if b[2][0] == 'o':
                streak_counter_d = 3

    if b[0][0] == 'o':
        if b[1][1] == 'o':
            if b[2][2] == 'o':
                streak_counter_d = 3
                    
    if streak_counter_i == 3:
        return True
    elif streak_counter_j == 3:
        return True
    elif streak_counter_d == 3:
        return True
    else:
        return False