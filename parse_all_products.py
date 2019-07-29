import pandas as pd
import os

if __name__ == '__main__':
    # data locations
    data_folderpath = '/home/hywu0110/fda_drug_approval/drugsatfda20190723'
    output_folderpath = '/home/hywu0110/fda_drug_approval/output'
    submission_filename = 'Submissions.txt'
    product_filename = 'Products.txt'
    biologics_filename = 'biologics.csv'
    # get approved submissions
    submission_df = pd.read_csv(
        os.path.join(data_folderpath, submission_filename),
        delimiter='\t',
        engine='python', # the default engine cannot handle some decoding issue
        index_col=False, # avoid extra delimiter before end-of-line issue
        )
    submission_df['SubmissionStatusDate'] = submission_df['SubmissionStatusDate'].apply(pd.to_datetime)
    # submission filters (see README.txt)
    sub_status_filter = submission_df['SubmissionStatus'].apply(lambda s: s in ['AP', 'TA'])
    sub_type_filter = submission_df['SubmissionType'] == 'ORIG'
    sub_class_filter = submission_df['SubmissionClassCodeID'].apply(lambda x: x in [7, 8])
    sub_filter = sub_status_filter & sub_type_filter & sub_class_filter
    column_of_interest = ['ApplNo', 'SubmissionStatusDate']
    submission_df = submission_df.loc[sub_filter, column_of_interest]
    # get approved products
    product_df = pd.read_csv(
        os.path.join(data_folderpath, product_filename),
        delimiter='\t',
        engine='python', # the default engine cannot handle some decoding issue
        index_col=False, # avoid extra delimiter before end-of-line issue
        )
    approved_product_df = product_df.merge(
        right=submission_df,
        how='inner',
        on='ApplNo',
        )
    column_of_interest = ['SubmissionStatusDate', 'DrugName', 'ActiveIngredient', 'Form']
    approved_product_df = approved_product_df[column_of_interest]
    approved_product_df.sort_values(
        by='SubmissionStatusDate',
        ascending=True,
        inplace=True,
    )
    approved_product_df.drop_duplicates(
        subset=['DrugName', 'ActiveIngredient'],
        inplace=True,
        keep='first',
        )
    # check if it's classified as biologics
    biologics_df = pd.read_csv(os.path.join(output_folderpath, biologics_filename))
    biologics_brand_name = set(
        [s.title() for s in biologics_df['brand_name'].tolist() if pd.notnull(s)]
    )
    approved_product_df['biologics'] = approved_product_df['DrugName'].apply(
        lambda s: s.title() in biologics_brand_name
    )
    # end of script
    approved_product_df.to_csv(
        os.path.join(output_folderpath, 'approved_product.csv'),
        index=False,
        )
    print('Done.')