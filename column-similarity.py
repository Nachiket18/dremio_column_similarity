import pandas as pd
import openclean_metanome.config as config
from openclean_metanome.download import download_jar
from openclean_metanome.algorithm.hyucc import hyucc

download_jar(verbose = True)

dict_num_tables = 0
dict_blocks = {}


def generate_k_mer(str_d, k:int):
    if len(str_d) <= k:
        return [str_d]

    return [str_d[i:i+k] for i in range(0, len(str_d)-(k-1))]

def do_blocking(de_duplicated_set: list,attribute_name, partition_blocks = True):
    global dict_num_tables
    
    for i in range(len(de_duplicated_set)):
        tmp = de_duplicated_set[i]
        k_mer_list = generate_k_mer(str(tmp[attribute_name]), 3)
        
        for asc in k_mer_list:
            if asc.lower() in dict_blocks:
                if partition_blocks:
                    if dict_num_tables not in dict_blocks[asc.lower()]:
                        dict_blocks[asc.lower()][dict_num_tables] = []
                    dict_blocks[asc.lower()][dict_num_tables].append(i)
                else:
                    dict_blocks[asc.lower()].append(i)
            else:
                if partition_blocks:
                    dict_blocks[asc.lower()] = {dict_num_tables: [i]}
                else:
                    dict_blocks[asc.lower()] = [i]
        
    dict_num_tables += 1

def get_uccs(df, max_ucc_size = 3, **kwargs):
    env = {config.METANOME_JARPATH: config.JARFILE()}
    
    keys = hyucc(df, env = env, max_ucc_size = max_ucc_size, **kwargs)
    
    return keys


def main():
    nation = pd.read_csv(filepath_or_buffer="./dataset/nation.tbl",delimiter='|', header = None)
    nation_columns = ["nationkey", "nationname", "regionkey", "comment", 'nan']
    nation.columns = nation_columns
    nation = nation.drop(columns=['nan'])

    customer = pd.read_csv("./dataset/customer.tbl",delimiter='|')
    customer_columns = ["customerkey", "name", "address", "nationkey", 'phone', 'acctbal', 'mktsegment', 'comment', 'nan']
    customer.columns = customer_columns
    customer = customer.drop(columns=['nan'])

    #print(nation.head())
    #print(customer.head())


    dependent_attribute = ['nationkey']
    reference_attribute = ['nationkey']

    do_blocking(customer.values.tolist(),7)
    print(len(dict_blocks))

    do_blocking(nation.values.tolist(),3)

    #new_blocks = partition_blocks(nation_blocks, customer_blocks)

    #print(dict_blocks.keys())
    #print(dict_blocks)
    example_key = 'the'
    print("Example key: ", example_key)
    #print("Example block: ", new_blocks[example_key])
    print("Number of blocks: ", [f"{k}: {len(v)}" for k, v in dict_blocks[example_key].items()])
    

    print("--------------UCCs--------------")

    customer_keys = get_uccs(customer)
    print("Customer UCCs:")
    for ucc in customer_keys:
        print(ucc)
        
    print()
    
    nation_keys = get_uccs(nation)
    print("Nation UCCs:")
    for ucc in nation_keys:
        print(ucc)

if __name__ == "__main__":
    main()