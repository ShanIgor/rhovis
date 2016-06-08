from  matplotlib import pyplot as plt
import numpy as np

model_fnames = {
    'crust': 'rho.crust{}.dat',
    'prem': 'rho.prem{}.dat',
}

import argparse
parser=argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--xlength', nargs=2, metavar=('MIN', 'MAX'),type=float)
group.add_argument('--xdepth', nargs=2, metavar=('MIN', 'MAX'),type=float)
parser.add_argument("--yrho",nargs=2,metavar=('MIN','MAX'),type=float)
parser.add_argument("--curve",type=int,required=True)
parser.add_argument("--model", choices=model_fnames.keys())
parser.add_argument("--plot-curves", action='store_true')
parser.add_argument("--plot-crust", action='store_true')
parser.add_argument("--plot-avg", action='store_true')
parser.add_argument("--plot-std", action='store_true')
parser.add_argument("--plot-min", action='store_true')
parser.add_argument("--plot-max", action='store_true')


args=parser.parse_args()
ax=plt.gca()
plt.minorticks_on()
if args.yrho is not None:
    ax.set_ylim(*args.yrho)

if args.xlength:
    min_length, max_length = args.xlength
    min_rho,max_rho=args.yrho
    plt.xlabel('length  (km)')
    plt.ylabel(r'$\rho$  (g/cm$^{3}$)')
    plt.title('Density distribution in Earth matter')

fname=model_fnames[args.model]
lall = []
funcs = []
for i in range(0,args.curve+1):
    rho, ls = np.loadtxt(fname.format(i),float), np.loadtxt('length{}.dat'.format(i),float)
    ls = np.hstack([-ls[ls<=0][0:-1], 2*ls.max()-ls[ls>=0][1:]])
    lall.append(ls)

    funcs.append(lambda l, ls=ls, rho=rho: rho[np.searchsorted(ls, l, side='right')-1])

    kwargs = {}
    if i == 0:
        kwargs['linewidth'] = 2
    if args.plot_curves or i == 0 and args.plot_crust:
        plt.plot(ls, rho, label=('crust' if i == 0 else None))
    ax.set_xlim(min_length, max_length)

lall = np.unique(sorted(np.hstack(lall)))
rhoall = []
for func in funcs:
    rhoall.append(func(lall))
rhoall = np.vstack(rhoall).T
rhoavg = rhoall.mean(axis=1)
if args.plot_avg:

    ax.plot(lall, rhoavg, label='average')
if args.plot_min:
    ax.plot(lall, np.amin(rhoall, axis=1), label='min')
if args.plot_max:
    ax.plot(lall, np.amax(rhoall, axis=1), label='max')
if args.plot_std:
    rhostd = rhoall.std(axis=1)
    ax.fill_between(lall, rhoavg-rhostd, rhoavg+rhostd, alpha=0.3)

plt.legend(loc='lower center')
if args.xdepth:
    rho, d = np.loadtxt("rho.dat"), np.loadtxt("depth.dat")
    min_depth, max_depth = args.xdepth
    min_rho,max_rho=args.yrho
    pmask = np.logical_and(min_depth < d, d <= max_depth)
    prho, pl = rho[pmask], d[pmask]
    mmask =np.logical_and(-max_depth <= d, d < -min_depth)
    mrho, ml = rho[mmask], d[mmask]

    plt.xlabel('depth  (km)')
    plt.ylabel(r'$\rho$  (g/cm$^{3}$)')
    plt.title('Density distribution in Earth matter')
    ax.set_xlim(-(max_depth-min_depth), max_depth-min_depth)
    plt.plot(ml-ml.max(), mrho)
    plt.plot(pl-pl.min(), prho)
    ticks = plt.xticks()[0]
    ticks[ticks<0] = -ticks[ticks<0]
    ticks+=min_depth

ax.grid(which='both')
ax.grid(which='minor', alpha=0.5)
ax.grid(which='major', alpha=0.5)

plt.show()
