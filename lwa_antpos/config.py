import dsautils.cnf as cnf
from pkg_resources import Requirement, resource_filename

CNFCONF = resource_filename(Requirement.parse("lwa_antpos"), "lwa_antpos/data/cnfConfig.yml")


def test():
    dd = {'test': 'hi'}
    my_cnf = cnf.Conf()
    my_cnf = cnf.Conf(data={'ant': dd}, cnf_conf=CNFCONF)
    print(f'Subsystems: {my_cnf.list()}')

    return my_cnf
