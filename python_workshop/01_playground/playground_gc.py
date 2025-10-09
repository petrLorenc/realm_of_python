import gc
import referrers

def main():
    gc.collect()
    other_var = {"my_key": {"my_value": "my_value"}}
    my_var = other_var["my_key"]
    print(referrers.get_referrer_graph(my_var))
    print(referrers.get_referrer_graph(other_var))

if __name__ == '__main__':
    main()