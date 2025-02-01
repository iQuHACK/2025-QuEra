

def cost(results:dict):
    alpha = .02
    beta = 0.5
    gamma = 1
    delta = 0.6
    n = 0.8
    touches = results.get('ntouches')
    g_cz = results.get('apply_global_cz')
    g_rz = results.get('apply_global_rz')
    g_xy = results.get('apply_global_xy')
    l_rz = results.get('apply_local_rz')
    l_xy = results.get('apply_local_xy')
    
    return alpha*(g_rz + g_xy) + beta*(l_rz + l_xy) + gamma*(g_cz) + n*(touches)
