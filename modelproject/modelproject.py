from scipy import optimize
import sympy as sm
import numpy as np
import matplotlib.pyplot as plt

def solve_for_ss(s,g,n,alpha,delta):
    """ solve for the steady state level of capital

    Args:
        s (float): saving rate
        g (float): technological growth rate
        n (float): population growth rate
        alpha (float): cobb-douglas parameter
        delta (float): capital depreciation rate 

    Returns:
        result (RootResults): the solution represented as a RootResults object

    """ 
    
    # a. define objective function
    f = lambda k: k**alpha
    obj_kss = lambda kss: kss - (s*f(kss) + (1-delta)*kss)/((1+g)*(1+n))

    #. b. call root finder
    result = optimize.root_scalar(obj_kss,bracket=[0.1,100],method='bisect')
    
    return result

def graph_lom(A_val, X_val, alpha_val, eta_val, mu_val, ss_func, lom_func,initial_L):
    """ graphs the law of motion for the malthus model

    Args:
        A (float):          technology level
        X (float):          amount of land
        alpha (float):      output elasticity of A*X
        eta (float):        birth preference/cost
        mu (float):         death rate
        ss_func (func):     steady state expression (must be lambdified)
        lom_func (func):    law of motion expression (must be lambdified)
    
    """

    # c. initializing figure
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)

    # b. data for plots
    ss_val = ss_func(A_val,X_val,alpha_val,eta_val,mu_val)
    L_t_array = np.linspace(0,ss_val*1.3,num=1000) # ss_val*1.3 ensures that the function is evaluated beyond ss
    L_t1_array = lom_func(L_t_array,eta_val,A_val,X_val,alpha_val,mu_val)

    # c. function plots
    ax.plot(L_t_array, L_t_array, label="$L_t = L_{t+1}$", color='red',linewidth=3) # 45 degree line
    ax.plot(L_t_array, L_t1_array, label="$L_{t+1}$", color='green',linewidth=3) # pop. law of motion

    # d. plotting steady state
    ss_val = ss_func(A_val,X_val,alpha_val,eta_val,mu_val)
    ax.vlines(ss_val, ymin = 0, ymax=ss_val, label='steady state', color="black")
    ax.hlines(ss_val, xmin = 0, xmax=ss_val, color="black")

    # e. plotting transition to steady state
    L_0 = initial_L*ss_val # L_0 chosen as percentage of ss
    L_1 = lom_func(L_0,eta_val,A_val,X_val,alpha_val,mu_val)
    L_2 = lom_func(L_1,eta_val,A_val,X_val,alpha_val,mu_val)

    ax.vlines(L_0, 0, L_1, color="black")
    ax.hlines(L_1, L_0, L_1, color="black")
    ax.vlines(L_1, L_1, L_2, color="black")
    ax.vlines(L_1, 0, L_1, linestyle='dotted', color="black")
    ax.hlines(L_2, L_1, (L_2-L_1)/2+L_1,linestyle='dashed',color="black")

    # f. design
    # i. labels for vertical lines
    shiftx, shifty = ss_val*0.015, ss_val*0.0425 # text shifts relative to ss absolute value
    plt.text(L_0-shiftx, -shifty, '$L_0$')
    plt.text(L_1-shiftx, -shifty, '$L_1$')
    plt.text(ss_val-shiftx, -shifty, '$L^*$') # label

    # ii. titles
    ax.set_xlabel("$L_t$")
    ax.set_ylabel("$L_{t+1}$")
    ax.legend(loc="upper left")

    # iii. axis/grid
    ax.grid()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()