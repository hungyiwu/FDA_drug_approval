import pandas as pd
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # data location
    data_folderpath = '/home/hywu0110/fda_drug_approval/output'
    data_filename = 'approved_product.csv'
    data_df = pd.read_csv(os.path.join(data_folderpath, data_filename))
    # process datetime
    data_df['SubmissionStatusDate'] = pd.to_datetime(data_df['SubmissionStatusDate'])
    data_df['year'] = data_df['SubmissionStatusDate'].apply(
        lambda t: t.to_pydatetime().year
    )
    yearly_count = data_df.groupby(
        by=['year', 'biologics'],
    )['DrugName'].agg(
        ['count'],
    ).reset_index()
    yearly_count.reset_index(inplace=True)
    yearly_count['modality'] = yearly_count['biologics'].apply(
        lambda b: 'Biologics' if b else 'Small molecules',
    )
    yearly_count = yearly_count[['year', 'modality', 'count']].pivot(
        index='year',
        columns='modality',
        values='count',
    ).reset_index().fillna(0)
    # cumulative sum
    yearly_count.sort_values('year', ascending=True, inplace=True)
    yearly_count['Small molecules'] = yearly_count['Small molecules'].cumsum()
    yearly_count['Biologics'] = yearly_count['Biologics'].cumsum()
    # plot
    print(yearly_count.columns)
    plt.plot(yearly_count['year'], yearly_count['Small molecules'])
    plt.plot(yearly_count['year'], yearly_count['Biologics'])
    plt.xlabel('year')
    plt.ylabel('cumulative approval')
    plt.legend(['Small molecules', 'Biologics'])
    plt.show()
    # end of script
    print('Done.')