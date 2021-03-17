import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

def u_func(c,h,phi=0.3): # equation 1
    """ 
    Equation (1) from the sheet (a Cobb-Douglas util func)
    Returns utility from consumption and housing

    Arguments:
    c:      consumption
    h:      housing
    phi:    preferences (default 0.3)

    """
    u = (c**(1-phi))*(h**phi)
    return u

def totalcost(ph,r=0.03,tg=0.012,tp=0.004,eps=0.5,pc=3): # equation 4
    """
    Returns the total cost of owning a house given by equation (4).

    Arguments:
    ph:     price of house
    r:      interest rate (default 0.03)
    tg:     general tax rate (default 0.012)
    tp:     progressive tax rate (default 0.004)
    eps:    public value factor (default 0.5)
    pc:     price cutoff taxation (default 3)

    """
    pv = ph*eps # public assessment value, given by eq. (2)
    totalcost = r*ph+tg*pv+tp*max(pv-pc,0)
    return totalcost

def houseprice(tc,r=0.03,tg=0.012,tp=0.004,eps=0.5,pc=3): 
    """
    Derives a houseprice from a totalcost. This function is used to
    create the upper bound when optimizing.

    Arguments:
    tc:     totalcost
    r:      interest rate (default 0.03)
    tg:     general tax rate (default 0.012)
    tp:     progressive tax rate (default 0.004)
    eps:    public value factor (default 0.5)
    pc:     price cutoff taxation (default 3)

    """
    # check if public valuation is above taxation cutoff and calculate backwards
    if tc > totalcost(pc/eps):  
        houseprice = (tc+pc*tp)/(r+eps*(tg+tp))
    else:
        houseprice = tc/(r+tg*eps)
    return houseprice

def u_max(phi=0.3,m=0.5,r=0.03,tg=0.012,tp=0.004,eps=0.5,pc=3):
    """
    Maximizes the u_func with respect to consumption and housing and
    returns a tuple of optimal consumption, housing and utility.

    Using the budget constraint, consumption is rewritten as an
    expression of housing.

    Arguments:
    phi:    preference (default 0.3)
    m:      cash-on-hand (budget default 0.5)
    r:      interest rate (default 0.03)
    tg:     general tax rate (default 0.012)
    tp:     progressive tax rate (default 0.004)
    eps:    public value factor (default 0.5)
    pc:     price cutoff taxation (default 3)

    """
    # a. objective function to be minimized
    def objective(h,phi,m,r,tg,tp,eps,pc):
        c = m-totalcost(h,r,tg,tp,eps,pc) # c as expressed by h
        return -u_func(c,h,phi)

    # b. call solver
    res = optimize.minimize_scalar(
        objective,method='Bounded',
        bounds=(0,houseprice(m,r,tg,tp,eps,pc)), # upper bound: entire budget spent on housing
        args=(phi,m,r,tg,tp,eps,pc))

    # c. unpack solution
    h_star = res.x
    c_star = m-totalcost(h_star)
    u_star = u_func(c_star,h_star,phi)

    return c_star, h_star, u_star

def print_solution(c,h,u,phi=0.3):

    text = ""

    # a. house value
    text += f'Optimal house value:\nh = {h:.4f}\n\n'
    
    # b. consumption
    text += f'Optimal consumption:\nc = {c:.4f}\n\n'

    # d. totalcost
    text += f'To be spent on housing:\ntau = {totalcost(h):.4f}\n\n'

    # c. utility
    text += f'Maximum utility:\nu = {u:.4f}'

    print(text)

def ch_figures(c_vals,h_vals,m_vals,m_range=None,c_range=None,h_range=None,
               mark_l=None,mark_r=None):
    """
    Plots two figures of optimum c* and h* values against the given budget.
    Ability to specify c,h and m axis-ranges and mark a point on each figure.

    Arguments:
    c_vals:             consumption values
    h_vals:             housing values
    m_vals:             budget values
    mark_l, mark_r:     coordinate tuple for left and right mark
    m_range, c_range, h_range:    axis ranges

    """
    plt.style.use("seaborn-whitegrid")

    # a. create the figure
    fig = plt.figure(figsize=(12,6)) # figsize is in inches

    # b. left plot
    ax_left = fig.add_subplot(1,2,1)
    ax_left.plot(m_vals,c_vals,c='blue',linewidth=2)

    ax_left.set_title('c* as function of m')
    ax_left.set_xlabel('cash-on-hands, $m$')
    ax_left.set_ylabel('optimal consumption, $c*$')
    ax_left.set_xlim(m_range)
    ax_left.set_ylim(c_range)
    ax_left.grid(True)

    if mark_l != None:
        ax_left.scatter(*mark_l,s=3000,edgecolors='red',
                        linewidths=1.5).set_facecolor("none")

    # c. right plot
        ax_right = fig.add_subplot(1,2,2)
    ax_right.plot(m_vals,h_vals,c='blue',linewidth=2)

    ax_right.set_title('h* as function of m')
    ax_right.set_xlabel('cash-on-hands, $m$')
    ax_right.set_ylabel('optimal housing, $h*$')
    ax_right.set_xlim(m_range)
    ax_right.set_ylim(h_range)
    ax_right.grid(True)

    if mark_r != None:
        ax_right.scatter(*mark_r,s=3000,edgecolors='red',
                         linewidths=1.5).set_facecolor("none")

    return fig

def avgtax(ba,r=0.03,tg=0.012,tp=0.004,eps=0.5,pc=3):
    """
    Takes an array of budgets and returns their average tax paid, when
    optimum housing is chosen based on the utility function u_func.

    Arguments:
    ba:     1D numpy budget array
    r:      interest rate (default 0.03)
    tg:     general tax rate (default 0.012)
    tp:     progressive tax rate (default 0.004)
    eps:    public value factor (default 0.5)
    pc:     price cutoff taxation (default 3)

    """

    sum = 0
    for mi in ba:
        paoh = u_max(m=mi,r=r,tg=tg,tp=tp,eps=eps,pc=pc)[1]*eps # public assessment value of optimal housing
        sum += tg*paoh+tp*max(paoh-pc,0)
    return sum/ba.size # sum is divided by number of households

def tg_finder(ba,target,r=0.03,tp=0.009,eps=0.8,pc=8):
    """
    Takes an array of budgets and target for average tax.
    Returns the general tax rate needed to keep avgtax = target.

    Arguments:
    ba:     1D numpy budget array
    target: target value for totaltax
    r:      interest rate (default 0.03)
    tp:     progressive tax rate (default 0.009)
    eps:    public value factor (default 0.8)
    pc:     price cutoff taxation (default 8)

    """
 
    # a. objective function to be minimized
    def objective(tg_new,ba,target,r,tp,eps,pc=pc):
        return np.abs(target - avgtax(ba,r,tg_new,tp,eps,pc)) # we want this difference to be 0

    # b. call solver
    res = optimize.minimize_scalar(objective,method='bounded',bounds=[0,1],
                                   args=(ba,target,r,tp,eps,pc),
                                   options={'xatol': 1e-09,}) # a low tolerance ensures a precise result

    return res.x