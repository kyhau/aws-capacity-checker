import json
from collections import defaultdict
from os import makedirs
from os.path import basename, join

import click

OUTPUT_DIR = 'html'
makedirs(OUTPUT_DIR, exist_ok=True)


def ec2_instance_type_per_name(actual, account):
    acc_ret = defaultdict(dict)

    for stack_name, details in actual.items():
        # ASG
        if 'AsgActual' in details['Actual']:
            for asg_name, values in details['Actual']['AsgActual'].items():
                name = asg_name

                acc_ret[name]['Desired'] = values['Desired']
                acc_ret[name]['Min'] = values['MinSize']
                acc_ret[name]['Max'] = values['MaxSize']
                acc_ret[name]['MixedInstancesPolicy'] = '' if values['MixedInstancesPolicy'] is None else ';'.join(values['MixedInstancesPolicy'])

                for instance_type, cnt in values['InstanceTypes'].items():
                    if instance_type not in acc_ret[name]:
                        acc_ret[name][instance_type] = 0
                    acc_ret[name][instance_type] += cnt

        elif 'EcsClusterActual' in details['Actual']:
            for cluster_name, values in  details['Actual']['EcsClusterActual'].items():
                if values['FargateOnly'] is False:
                    print(f'TODO should not be here: {stack_name} {cluster_name}')

        # EC2
        if 'Ec2Actual' in details['Actual']:
            name = stack_name

            items = details['Actual']['Ec2Actual'].get('InstanceTypes', {})
            for instance_type, cnt in items.items():
                if instance_type not in acc_ret[name]:
                    acc_ret[name][instance_type] = 0
                acc_ret[name][instance_type] += cnt


    # account, name, ec2, instanceType, cnt
    csv_data = []
    for name, data in acc_ret.items():
        min_v, desired_v, max_v = (data['Min'], data['Desired'], data['Max']) if 'Min' in data else (0, 0, 0)
        mixed_p = data.get('MixedInstancesPolicy', '')
        for instance_type, cnt in data.items():
            if instance_type not in ['Min', 'Max', 'Desired', 'MixedInstancesPolicy']:
                csv_data.append([account, name, 'ec2', instance_type, str(min_v), str(cnt), str(max_v), mixed_p])
                if desired_v > 0 and cnt != desired_v:
                    print('Warning cnt != desired_v: ', account, name, instance_type, cnt, desired_v)

    report_file = join(OUTPUT_DIR, 'ec2_capacity.csv')
    with open(report_file, 'w') as f:
        f.write('Account,Name,EC2,InstanceType,Min,Desired,Max,MixedInstancesPolicy\n')
        for line in csv_data:
            f.write(f'{",".join(line)}\n')


def rds_instance_type_per_name(actual, account):
    acc_ret = defaultdict(dict)

    for stack_name, details in actual.items():

        if 'RdsClusterActual' in details['Actual']:
            for cluster_name, values in details['Actual']['RdsClusterActual'].items():

                if values['EngineMode'] in ['serverless']:
                    continue

                name = cluster_name

                for instance_type, cnt in values['InstanceTypes'].items():
                    if instance_type not in acc_ret[name]:
                        acc_ret[name][instance_type] = 0
                    acc_ret[name][instance_type] += cnt

        elif 'RdsActual' in details['Actual']:
            name = stack_name

            items = details['Actual']['RdsActual'].get('InstanceTypes', {})
            for instance_type, cnt in items.items():
                if instance_type not in acc_ret[name]:
                    acc_ret[name][instance_type] = 0
                acc_ret[name][instance_type] += cnt

    # account, name, rds, instanceType, cnt
    csv_data = []
    for name, data in acc_ret.items():
        for instance_type, cnt in data.items():
            csv_data.append([account, name, 'rds', instance_type, str(cnt)])

    report_file = join(OUTPUT_DIR, 'rds_capacity.csv')
    with open(report_file, 'w') as f:
        f.write('Account,Name,RDS,InstanceType,Min,Desired,Max,MixedInstancesPolicy\n')
        for line in csv_data:
            f.write(f'{",".join(line)}\n')


def elb_per_name(actual, account):
    acc_ret = defaultdict(dict)

    for stack_name, details in actual.items():

        if 'RdsClusterActual' in details['Actual']:
            for cluster_name, values in details['Actual']['RdsClusterActual'].items():

                if values['EngineMode'] in ['serverless']:
                    continue

                name = cluster_name

                for instance_type, cnt in values['InstanceTypes'].items():
                    if instance_type not in acc_ret[name]:
                        acc_ret[name][instance_type] = 0
                    acc_ret[name][instance_type] += cnt

        elif 'RdsActual' in details['Actual']:
            name = stack_name

            items = details['Actual']['RdsActual'].get('InstanceTypes', {})
            for instance_type, cnt in items.items():
                if instance_type not in acc_ret[name]:
                    acc_ret[name][instance_type] = 0
                acc_ret[name][instance_type] += cnt

    # account, name, rds, instanceType, cnt
    csv_data = []
    for name, data in acc_ret.items():
        for instance_type, cnt in data.items():
            csv_data.append([account, name, 'rds', instance_type, str(cnt)])

    report_file = join(OUTPUT_DIR, 'elb_capacity.csv')
    with open(report_file, 'w') as f:
        for line in csv_data:
            f.write(f'{",".join(line)}\n')


@click.command()
@click.argument('input_file')
def main(input_file):
    with open(input_file, 'r') as f:
        actual = json.load(f)

    account_name = basename(input_file).split('.')[0]

    ec2_instance_type_per_name(actual, account_name)
    #rds_instance_type_per_name(actual, account_name)
    #elb_per_name(actual, account_name)


if __name__ == '__main__':
     main()
