import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

if __name__ == '__main__':
    # data location
    data_folderpath = '/home/hywu0110/FDA_drug_approval/processed_data'
    output_folderpath = '/home/hywu0110/FDA_drug_approval'
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
    yearly_count.reset_index(inplace=True, drop=True)
    yearly_count['Small molecules'] = yearly_count['Small molecules'].cumsum()
    yearly_count['Biologics'] = yearly_count['Biologics'].cumsum()
    # plot
    plt.rcParams.update({'font.size': 18})
    plt.plot(yearly_count['year'], yearly_count['Small molecules'], linewidth=3)
    plt.plot(yearly_count['year'], yearly_count['Biologics'], linewidth=3)
    # annotation
    last_index = yearly_count.index[-1]
    x = yearly_count.loc[last_index, 'year']
    y = yearly_count.loc[last_index, 'Small molecules']
    plt.text(s=str(int(y)), x=x, y=y+100, ha='center')
    plt.plot([x], [y], marker='^', markerfacecolor='k', markeredgecolor='k')
    y = yearly_count.loc[last_index, 'Biologics']
    plt.text(s=str(int(y)), x=x, y=y+100, ha='center')
    plt.plot([x], [y], marker='^', markerfacecolor='k', markeredgecolor='k')
    plt.xlabel('Year')
    plt.text(s='FDA new drug approval (cumulative)\n'
            'as of July 23rd, 2019\n'
            'source: www.fda.gov',
            x=1940, y=1200, ha='left', fontsize=16, linespacing=1.5)
    plt.legend(['Small molecules', 'Biologics'], frameon=False, loc='center left')
    # decoration
    plt.yticks([])
    ladder = range(1940, 2021, 20)
    plt.xticks(ticks=ladder, labels=ladder)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(10))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folderpath, 'figure_1.png'))
    # end of script
    print('Done.')
