from  matplotlib import pyplot as plt
import numpy as np
import argparse

m2km=1000.0
parser=argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--xlength', nargs=2, metavar=('MIN', 'MAX'),type=float)
group.add_argument('--xdepth', nargs=2, metavar=('MIN', 'MAX'),type=float)
parser.add_argument("--yrho",nargs=2,metavar=('MIN','MAX'),type=float)
args=parser.parse_args()

if args.xlength:
    ls=np.loadtxt('length0.dat')
    rho_prem=np.loadtxt('rho.prem0.dat')
    rho_crust=np.loadtxt('rho.crust0.dat')
    rho_eff=np.loadtxt('rho.effective.dat')
#    rhomin=np.loadtxt('rho.min.dat')
#    rhomax=np.loadtxt('rho.max.dat')
    min_length, max_length = args.xlength
    min_rho,max_rho=args.yrho
    lall = []
    funcs = []

    ls = np.hstack([-ls[ls<=0][0:-1], 2*ls.max()-ls[ls>=0][1:]])
    lall.append(ls)

    funcs.append(lambda l, ls=ls, rho_prem=rho_prem: rho_prem[np.searchsorted(ls, l, side='right')-1])
    plt.rc('font', weight='bold')
    plt.rc('xtick.major', size=5, pad=7)
    plt.rc('xtick', labelsize=10)
    plt.axis([min_length,max_length,min_rho,max_rho])
    plt.xlabel('L,  km')
    plt.ylabel(r'$\rho$,  g/cm$^{3}$')
    #plt.rc('text', usetex=True)


    #plt.title('Densities')
    pl=plt.plot(ls,rho_prem,label='PREM',linewidth=2,linestyle='--',
                color='black')
    pl=plt.plot(ls,rho_crust,label='CRUST',linewidth=2,linestyle='-',
                color='black')
    pl=plt.plot(ls,rho_eff,label=r'Effective density',linewidth=2,
                linestyle='dashdot',color='black')
    pl=plt.fill_between(ls,rho_eff-0.06,rho_eff+0.06,alpha=0.8,
                        facecolor='black')
 #   pl=plt.plot(ls,rhomin,label=r'MIN density',linewidth=2)
 #   pl=plt.plot(ls,rhomax,label=r'MAX density',linewidth=2)

if args.xdepth:
    x=np.loadtxt('xdepth.prem.dat')/m2km
    y=np.loadtxt('yrho.prem.dat')
    min_depth, max_depth = args.xdepth
    min_rho,max_rho=args.yrho
    plt.axis([min_depth,max_depth,min_rho,max_rho])
    plt.xlabel('depth  km')
    plt.ylabel(r'$\rho$  g/cm$^{3}$')
    #plt.title('Densities')
    pl=plt.plot(x,y,label='PREM')

ax=plt.gca()
plt.minorticks_on()
ax.legend(loc='upper right')


ax.grid(which='both')

ax.grid(which='minor', alpha=1)
ax.grid(which='major', alpha=0.5)

plt.show()
