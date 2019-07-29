import pandas as pd
import re
import os

if __name__ == '__main__':
    # data locations
    data_folderpath = '/home/hywu0110/fda_drug_approval'
    output_folderpath = '/home/hywu0110/fda_drug_approval/output'
    bio_filename = 'fda_biologics_list.csv'
    # define regular expression patterns
    approval_date_pattern = r'\d{2}\/\d{2}\/\d{2}'
    BLASTN_pattern = r'\d{6}'
    brand_name_pattern = r'\b[A-Z].*?\b' # see README.txt for StackOverflow reference
    generic_name_pattern = r'\b[a-z].*?\b' # derived from the brand name pattern
    # parse data
    with open(os.path.join(data_folderpath, bio_filename), 'r') as bio_file:
        lines = bio_file.readlines()[1::]
    record = []
    for line in lines:
        approval_date = re.findall(approval_date_pattern, line)[0]
        subline = line.split(approval_date)[0]
        BLASTN = re.findall(BLASTN_pattern, subline)[0]
        brand_name = ' '.join(re.findall(brand_name_pattern, subline))
        generic_name = ' '.join(re.findall(generic_name_pattern, subline))
        record.append({
            'approval_date':pd.to_datetime(approval_date, format='%m/%d/%y'),
            'BLASTN':BLASTN,
            'brand_name':brand_name,
            'generic_name':generic_name,
        })
    bio_df = pd.DataFrame.from_records(data=record)
    # end of script
    bio_df.to_csv(os.path.join(output_folderpath, 'biologics.csv'))
    print('Done.')