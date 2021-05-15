from scipy import optimize
import sympy as sm
import numpy as np
import matplotlib.pyplot as plt

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
        initial L (float):  initial population as percentage of steady state level (where 1.0 is equal to steady state)
    """

    # c. initializing figure
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)

    # b. data for plots
    ss_val = ss_func(A_val,X_val,alpha_val,eta_val,mu_val)
    L_t_array = np.linspace(0,ss_val*1.3,num=1000) # ss_val*1.3 ensures that the function is evaluated beyond ss
    L_t1_array = lom_func(L_t_array,A_val,X_val,alpha_val,eta_val,mu_val)

    # c. function plots
    ax.plot(L_t_array, L_t_array, label="$L_t = L_{t+1}$",linewidth=3) # 45 degree line
    ax.plot(L_t_array, L_t1_array, label="Law of motion ($L_{t+1}$)",linewidth=3) # pop. law of motion

    # d. plotting steady state
    ss_val = ss_func(A_val,X_val,alpha_val,eta_val,mu_val)
    ax.vlines(ss_val, ymin = 0, ymax=ss_val, color="black")
    ax.hlines(ss_val, xmin = 0, xmax=ss_val, color="black")

    # e. plotting transition to steady state
    L_0 = initial_L*ss_val # L_0 chosen as percentage of ss
    L_1 = lom_func(L_0,A_val,X_val,alpha_val,eta_val,mu_val)
    L_2 = lom_func(L_1,A_val,X_val,alpha_val,eta_val,mu_val)

    ax.vlines(L_0, 0, L_1, color="black")
    ax.hlines(L_1, L_0, L_1, color="black")
    ax.vlines(L_1, L_1, L_2, color="black")
    ax.vlines(L_1, 0, L_1, linestyle='dotted', color="black")
    ax.hlines(L_2, L_1, (L_2-L_1)/2+L_1,linestyle='dashed',color="black")

    # f. labels for transition lines
    shiftx, shifty = ss_val*0.015, ss_val*0.0425 # text shifts relative to the ss absolute value
    plt.text(L_0-shiftx, -shifty, '$L_0$')
    plt.text(L_1-shiftx, -shifty, '$L_1$')
    plt.text(ss_val-shiftx, -shifty, '$L^*$')

    # g. titles
    ax.set_xlabel("$L_t$")
    ax.set_ylabel("$L_{t+1}$")
    ax.legend(loc="upper left")


    # h. axis/grid
    ax.grid()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()