# -*- coding:utf-8 -*-
# @Time    : 2020/10/28 11:00
# @Author  : Heying Zhu

'''
generate two files CiteSpace needed
Synonym merge file (citespace.alias)
Exclude files (citespace.exclusion)
'''

# citespace.alias
'''
@PHRASEHypera postica#@PHRASEalfalfa weevil
@PHRASEalfalfa#@PHRASEmedicago sativa
'''
def generate_citespace_alias():

    the_path = "D:/data/thesaurus/alfalfa.the"    # the Synonym cleaning table
    save_path = "D:/data/citespace/citeSpace_alias.txt"  # save path
    alias_content = ""

    with open(the_path, "r") as f:
        lines = f.readlines()

    normal = ""
    for line in lines:
        line = line.replace("\\", "")
        if line.startswith("**"):
            if line[2:-1].isupper():
                normal = line[2:-1].lower()
            else:
                normal = line[2:-1]
        if line.startswith("0 1 ^"):
            alia = line[5:-2]
            if alia.isupper():
                alia = alia.lower()
            if normal != alia:
                alias_content = alias_content + "@PHRASE" + normal + "#@PHRASE" + alia + "\n"

    with open(save_path, "w") as f:
        f.write(alias_content)


# citespace.exclusion
'''
@PHRASE*
*为要排除的词
'''
def generate_citespace_exclusion():
    common_word = ["alfalfa (Medicago sativa L.)", "alfalfa", "medicago truncatula", "plant", "growth", "arabidopsis",
                   "legume", "arabidopsis thaliana", "identification", "medicago", "maize", "system", "medicago sativa l",
                   "wheat", "alfalfa seed", "truncatula"]
    save_path = "D:/data/citespace/citeSpace_exclusion.txt"
    content = ""

    for item in common_word:
        content = content + "@PHRASE" + item + "\n"

    content = content[:-1]
    with open(save_path, "w") as f:
        f.write(content)



if __name__ == '__main__':
    # generate_citespace_alias()
    generate_citespace_exclusion()
