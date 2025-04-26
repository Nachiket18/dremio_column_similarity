import pandas as pd


dict_blocks = {}


def generate_k_mer(str_d, k:int):
    if len(str_d) <= k:
        return [str_d]

    return [str_d[i:i+k] for i in range(0, len(str_d)-(k-1))]

def do_blocking(de_duplicated_set: list,attribute_name):

    for i in range(len(de_duplicated_set)):
        tmp = de_duplicated_set[i]
        k_mer_list = generate_k_mer(str(tmp[attribute_name]), 3)

        for asc in k_mer_list:
            if asc.lower() in dict_blocks:
                dict_blocks[asc.lower()].append(i)
            else:
                dict_blocks[asc.lower()] = [i]

def main():
    nation = pd.read_csv(filepath_or_buffer="/home/nachiket/dremio_use_case/dataset/nation.tbl/nation.tbl",delimiter='|', header = None)
    nation_columns = ["nationkey", "nationname", "regionkey", "comment", 'nan']
    nation.columns = nation_columns
    nation = nation.drop(columns=['nan'])

    customer = pd.read_csv("/home/nachiket/dremio_use_case/dataset/nation.tbl/customer.tbl/customer.tbl",delimiter='|')
    customer_columns = ["customerkey", "name", "address", "nationkey", 'phone', 'acctbal', 'mktsegment', 'comment', 'nan']
    customer.columns = customer_columns
    customer = customer.drop(columns=['nan'])

    print(nation.head())
    print(customer.head())


# keys = hyucc(nation, max_ucc_size=3, env=env)

# for ucc in keys:
#     print(ucc)

    dependent_attribute = ['nationkey']
    reference_attribute = ['nationkey']

    do_blocking(customer.values.tolist(),3)
    print(len(dict_blocks))


if __name__ == "__main__":
    main()