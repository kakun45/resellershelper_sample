from datetime import datetime
import geopandas as gpd
import numpy as np
import pandas as pd

import data
import read_file
import sanitize
import sr_graph1
import sr_numbers1
import utils

# for SALES REPORT
parties_filename = 'data/parties.csv'  # for 2019 MUST have col 'Brand Party'
parties_filename_20 = 'data/parties_2020_2ndhalfyear.csv'


def vis_department(sr_df, meta, head=6, sort_by_count=True, ascending=False, index=False):
    """
    HTML Displays 1st 'head' num rows of 'hi-to-lo' values for a graph above.
    
    :param sr_df: sales report raw df. df must have 'Department','Net Earnings' cols
    :param meta: metadata
    :param head: int(): num of rows to show, must be num>0 to show rows, col titles are shown if head(0)
    :param sort_by_count: flag which col to display 'hi to lo' on, on 'count' 1st or on 'mean'
    :param ascending: default=False => 'hi to lo' order
    :param index: show/hide index col. default=False, meaning: 'hide'
    :return: <IPython.core.display.HTML object> to display
    """
    sr_df2 = sanitize.clean_net_col(sr_df)  
    # group and agg
    df_group = sr_df2.groupby('Department')['Net Earnings'].agg(['count', 'mean']).reset_index()
    df_group = sanitize.round_df(df_group)
    # rename in place
    df_group.rename({'count': 'Count (Orders)', 'mean': 'Mean ($Net Earnings)'}, axis=1, inplace=True)
    df_sorted_count = utils.sort_df(df_group, ['Count (Orders)'], ascending=ascending)
    df_sorted_mean = utils.sort_df(df_group, ['Mean ($Net Earnings)'], ascending=ascending)
    # graph 
    sr_graph1.sold_by_department(sr_df, meta)
    if sort_by_count:
        return utils.html_table(df_sorted_count, meta, head=head, index=index, filename='vis_department.html')
    else:
        return utils.html_table(df_sorted_mean, meta, head=head, index=index, filename='vis_department.html')


def vis_cat_subcat(sr_df, meta, ir_df=None, cat=True, head=6, tail=6, ascending=False, index=False):
    """
    HTML Displays 1st 'head' num rows of 'hi to lo' values for a graph above.

    :param sr_df: sr_df raw. df must have 'Category','Subcategory','NWT' cols.    
    :param meta: meta
    :param head: int()/None: num of rows to show, must be num>0 to show rows, col titles are shown if head(0)
    :param tail: int()/None: num of rows to show, must be num>0,
    :param cat: default=True for 'Category'; cat=False for 'Subcategory' display
    :param ascending: default=False => 'hi to lo' order
    :param index: show/hide index col. default=False, meaning: 'hide'
    :return: <IPython.core.display.HTML object> to display; exports into html code tables
    """
    if cat:
        ser_group = sr_graph1.sold_by_category(sr_df, meta)  # => pandas.core.series.Series
    else:
        ser_group = sr_graph1.sold_by_subcategory(sr_df, meta)  # => pandas.core.series.Series
    ser_group_sorted = utils.sort_series(ser_group, ascending=ascending) 
    df1 = ser_group_sorted.to_frame().reset_index()  # convert ser to df in order to use HTML attr
    df1.rename({'NWT': 'Count'}, axis=1, inplace=True)  

    if cat:
        if ir_df:
            # cat and ir_df are both truthy
            # call sell_THROUGH to calc a new col 'STR' for head of cat like: #df['a'] = df['a'].apply(lambda x: x + 1)
            df1['STR'] = df1['Category'].map(lambda a: sr_numbers1.sell_through_rate(sr_df, ir_df, cat=a)).round(2)
            return utils.html_table(df1, meta, head=head, tail=None, index=index, filename='vis_cat_head.html'), \
                   utils.html_table(df1, meta, head=None, tail=tail, index=index, filename='vis_cat_tail.html')
        else:
            pass  # cat is True, ir_df is None
    else:
        if ir_df:
            pass  # cat is False, ir_df is not None
        else:
            pass  # cat is False, ir_df is None

    if ir_df and cat:
        pass  # cat and ir_df are both truthy

    elif ir_df and not cat:
        pass 
    elif cat and not ir_df:
        # First/last N rows of max/min values for a graph above
        return utils.html_table(df1, meta, head=head, tail=None, index=index, filename='vis_cat_head.html'), \
               utils.html_table(df1, meta, head=None, tail=tail, index=index, filename='vis_cat_tail.html')
    elif (not cat) and ir_df is None:
        # First/last N rows of max/min values for a graph above
        return utils.html_table(df1, meta, head=head, tail=None, index=index, filename='vis_subcat_head.html'), \
               utils.html_table(df1, meta, head=None, tail=tail, index=index, filename='vis_subcat_tail.html')
    else:
        raise ValueError("unpredicted value")


def vis_category_trees(sr_df, meta, head=5, ascending=False, index=False):
    """
    The trees show how far datapoints are from each other. Their frequency inside the cat. Prepare data for graph:
    :param sr_df: sales_report raw df
    :param head: number of Top Categories to display on graph, default=5. must be num>0. Don't pass more than 5 - legend gets too werbose
    :param ascending: Direction of sort in sr_df2 by Category count, default=False [from higher to lower] 
    :param index: show/hide index col. default=False, meaning: 'hide'
    :return: <IPython.core.display.HTML object> to display; exports into html code table
    """
    # make df of TopCat: group, count, sort, reset, drop
    sr_df2 = sr_df.groupby('Category').NWT.count().sort_values(ascending=ascending)
    # ABSOLUTELY VITAL THAT 'CATEGORY' OF THIS DF1 IS UNIQUE, IT WILL DOUBLE CAT IN MAIN DF:
    df1 = sr_df2.to_frame().reset_index().head(head)
    df1.rename({'NWT': 'Count'}, axis=1, inplace=True)  
    df11 = df1.drop(['Count'], axis=1)  # get only 1 col of Top Categories names df

    df22 = pd.merge(left=sr_df, right=df11, how='inner', on="Category")
    # make a new col looking: 'Accessories - Belts'
    df22['Category_Subcategory'] = df22['Category'].fillna('') + ' - ' + df22['Subcategory'].fillna('')
    # sort for legend to be ordered alpha.-ly, True sorts A->Z 
    df33 = df22.sort_values(by=['Category'], ascending=True)  
    # clean only one col 'Net Earn-s'
    df33_clean = sanitize.clean_net_col(df33)  
    # Order of Trees on x-axis
    order = df11['Category'].values.tolist() 
    # graph 'modified' sr_df
    sr_graph1.category_trees(df33_clean, meta, order)  
    return order, utils.html_table(df1, meta, head=head, index=index, filename='vis_cat_frequency_trees.html')


def vis_partying_brands(parties_csv, meta, sr_df, freq="M", head=13, index=True):
    """
    Merges parties_csv with sr_df, and adds 1/0 col for sold party/non-party brands to returned sr_df2.
    Takes parties_csv file with 'Brand' listed in the [0] col ONLY!
    :param parties_csv: .csv or db that carry all partying brands. Posh parties file, todo - keep it updated by new Bot logig parties
        Party_year: default=behavior for 2019 and earlier; half a 2020 through has hanged the list of parties,
                    for 2020 the format of .csv has changed, use party_year=2020 for changed type for new csv,
                    so need to check to add an extra cleanup steps for year or 2020 parties_csv.
    :param sr_df: sales_report df
    :param head: int(): MUST BE 12*1+1=13 for max of 1 years show, beginning with 12: 12-1-2...-12. For 3y and up
                    charge 10%+ and chamge party_csv to {2019:brands, 2020:Brands}
    :param freq: str(): freq="M" default as frequency month: 'M' # can be set to: 'D', 'W', 'M', 'Q', 'Y'
                    or all the list: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    :param index: Bool: it was a date in there, reset, now int.
    :return:  <IPython.core.display.HTML object> to display; exports into html code table
    """
    # process parties_csv: takes only 1st col from file and header=0
    posh_parties = pd.read_csv(parties_csv, usecols=[0], engine='python')  
    posh_parties.columns = ["Brand"]  # this col must be renamed this way, otherwise won't work for input file

    min_date = datetime(2020, 1, 1)
    middle_date = meta.sr_middle_date
    assert 'datetime' == middle_date.__class__.__name__  # to check if datetime obj, not int!

    if min_date <= middle_date:  
        # must ungroup the values with commas in a 2020 file
        brands_2020 = posh_parties.assign(Brand=posh_parties['Brand'].str.split(',')).explode('Brand')
        posh_parties = brands_2020
        # explode() takes too long! I've an alternative solution below: works faster!
        # run on a command line: cat Parties_new_1col\ \(1\).csv | sed 's/"//g' | tr , "\n" > my_new_file.csv

    posh_parties = sanitize.lower_brand_df(posh_parties)  # clean up white spaces either 2019 or -20, & lower() Brands
    # process sr_df
    sr_df2 = sanitize.lower_brand_df(sr_df)  # clean up sr_df2["Brand"] strip & lower all Brands
    sr_df2['Partying Brand'] = sr_df2.Brand.isin(posh_parties["Brand"]).astype(int)  # add a new col 1/0 into sr_df2
    sr_df3 = sanitize.date_normalizer(sr_df2, meta)  # converts str 'date' col into date obj
    sr_df4 = sanitize.clean_col(sr_df3, meta)  # deep cleans up lots of col's trash like '?', '$'
    sr_df5 = sr_df4[["Order Date", "Net Earnings"]]  # isolate 2 col
    sr_df6 = sr_df5.set_index('Order Date').groupby(pd.Grouper(freq=freq)).sum()  # group on 'order date', set as index
    party_sales = sr_df4.loc[sr_df4['Partying Brand'] == 1]  # isolate party brands sales only

    party_sales2 = party_sales[["Order Date", "Net Earnings"]] 
    party_sales3 = party_sales2.set_index('Order Date').groupby(pd.Grouper(freq=freq)).sum()

    joined_df = sr_df6.join(party_sales3, on="Order Date", how="outer", lsuffix='_total', rsuffix='_partying').fillna(0)

    joined_rounded_df = joined_df.round(2)  # finance: df.round(2) float b4 show any this data
    sr_graph1.partying_brands_in_sales(meta, joined_rounded_df, fontsize=12)
    joined_round_reset_df = joined_rounded_df.reset_index()
    return utils.html_table(joined_round_reset_df, meta, head=head, index=index, filename='vis_partying_brands.html')


def vis_highest_net_brands(sr_df, meta, head=7, ascending=False, index=False):
    """
    Highest Net Earnings (by Net Sales margin) Brand total, Dollar Amount: HNEBT for short. 

    :param sr_df: sr_df - raw sales report df must have 'Brand','Net Earnings' cols., and 'Listing Date', 'Order Date' to clean
    :param meta: metadata
    :param head: int(): num of rows to show, must be num>0 to show rows, col titles are shown if head(0)
    :param ascending: default=False => 'hi to lo' order
    :param index: show/hide index col. default=False, meaning: 'hide'
    :return: <IPython.core.display.HTML object> # First N rows of max values for a graph
    """
    sr_df2 = sanitize.lower_brand_df(sr_df)  # Must lower 'Brand' first
    sr_df3 = sanitize.clean_net_col(sr_df2)  # clean only one col 'Net Earn-s'
    sr_df4 = sanitize.date_normalizer(sr_df3, meta)  # clean up dates
    # group & sum 'Net Earnings' for vis. No need clean dates
    hnebt = utils.grouping_sum2(
        sr_df3,
        group_col=['Brand'],
        sum_col=['Net Earnings'],
        new_col=['Net Sales by Brand, $']
    ) 
    # limited (head) of df rows to return html
    df_sorted = utils.sort_df(hnebt, ['Net Sales by Brand, $', 'Brand'], ascending=ascending).round(2).head(head)

    all_brands = df_sorted.Brand.unique()  # 'numpy.ndarray' of only head(head) num of top brands

    sr_df4['year_month'] = pd.to_datetime(sr_df4['Order Date'], format='%Y-%m').dt.strftime(
        '%Y-%m')  # new 'yyyy-mm' col
    brand_sales = utils.grouping_sum2(
        sr_df4,
        group_col=['Brand', 'year_month'],
        sum_col=['Net Earnings'],
        new_col=['Net_Earnings_by_Brand']
    )  # group & sum 'Net Earnings' for graph
    # Didn't use Grouper, so ascending=True is responsible for order of x ticks: 2019-12(Left) > 2020-11(Right):
    brand_sales_sorted = brand_sales.sort_values(by=['year_month', 'Brand'], ascending=True).round(2)
    sr_graph1.highest_net_brands(meta, brand_sales_sorted, all_brands, fontsize=12)  # graph 'sorted' df
    return all_brands, utils.html_table(df_sorted, meta, head=head, index=index, filename='vis_highest_net_brands.html')


def vis_birthday_cake(meta, sr_df, head=3, tail=None, index=True):
    """
    Groups & 'summs' each line of sr_df in 'Net sales' by 'Department', frequency='Y' -> 'Year'
    takes life long lasting reports, ex. sr_df3year + 3dummies rows.
    
    :param meta: metadata
    :param sr_df: raw df of sales report
    :param head: int() or None: num of col to display, default=3, if there will be more than 5 years(df.head()
                has default 3 -> todo note the LIMIT for graphs are: 3 years .head(3) & iloc[:,:head], not for thml tho
    :param tail: int() or None: ,--> I need to pass tail=None for logic to do df only VS df.tail() or df.head()
    :param index: bool: show/hide, here default=True(show) coz it's a date in there, or a sequence number
    """
    sr_df1 = sanitize.clean_net_col(sr_df)  
    sr_df2 = sanitize.date_normalizer(sr_df1, meta) 
    selection = sr_df2[["Order Date", "Department", "Net Earnings"]]  
    data_mapped = selection.set_index('Order Date')
    data_mapped.index = data_mapped.index.year

    sr_df3 = data_mapped.groupby(['Order Date', "Department"])["Net Earnings"].sum().unstack().head(head)
    sr_graph1.birthday_cake(meta, sr_df3)  # stacked-up
    sr_df4 = data_mapped.groupby(["Department", 'Order Date'])["Net Earnings"].sum().unstack().iloc[:,
             :head]  # for limit 3 col-s, or head() head=None MUST be for all col-s
    sr_graph1.birthday_cake(meta, sr_df4, stacked=False)  # unstacked
    # same table just repeating lines of years, not agreagate them
    data_mapped2 = utils.grouping_sum2(
        data_mapped,
        group_col=['Order Date', 'Department'],
        sum_col=['Net Earnings'],
        new_col=["Net Earnings SUM, USD"])
    # adjust cake date for a lineplot. these are only 3 totals numbers!
    data_mapped3 = utils.grouping_sum2(
        selection,
        group_col=['Order Date'],
        sum_col=['Net Earnings'],
        new_col=["Net Earnings SUM, USD"])
    sr_graph1.heartbeat_of_sales(meta, data_mapped3)
    return utils.html_table(sr_df3, meta, head=head, tail=tail, index=index, filename='vis_birthday_cake.html'), \
           utils.html_table(data_mapped2, meta, head=None, tail=None, index=index,
                            filename='vis_birthday_cake_unstacked.html')  # here it displays everything, not just 3yrs


def vis_total_fees_paid(meta, sr_df, head=7, ascending=False, index=False):
    sr_df1 = sanitize.clean_price_col(sr_df, 'Net Earnings')  
    sr_df2 = sanitize.clean_price_col(sr_df1, 'Order Price')
    sr_df3 = sanitize.clean_price_col(sr_df2, 'Seller Shipping Discount')
    # defines colormap
    sr_df3['Total % of fees'] = 100 - ((sr_df3['Net Earnings'] / sr_df3['Order Price']) * 100)
    sr_graph1.total_fees_paid(meta, sr_df3)
    sr_df3["totalfees"] = sr_df3["Total % of fees"].round(0).astype(int)
    sr_df5 = sr_df3.groupby("totalfees").NWT.count().sort_values(ascending=ascending).to_frame().reset_index()
    sr_df5.rename({'totalfees': 'Total % of fees'}, axis=1, inplace=True)
    sr_df5.rename({'NWT': 'Count (Orders)'}, axis=1, inplace=True)
    return utils.html_table(sr_df5, meta, head=head, index=index, filename='vis_total_fees_paid.html')


def vis_net_sales_density(meta, sr_df, head=10, index=False):
    """
    Using geopandas creates a density map of sales via U.S. states cleans data, loads lat,lon, shapefile & calls 2 plots

    :param meta: metadata
    :param sr_df: raw df of sales report
    :param head: int() or None: num of col to display, default=10, 10-top best states(df.head(10)
                default -> todo note the LIMIT for graphs are: 10-best states
    :param index: bool: show/hide, here default=False(hide) coz it's a gdf with un-reset ##s in there
    :return: <IPython.core.display.HTML object> # First N rows of max values for a graph
    """
    initial_net_earn_col = 'Net Earnings'
    # lat, lon for geograph
    latlon = pd.read_csv('data/us-zip-code-latitude-and-longitude.csv', sep=';')
    # latlon df doesn't have dashes in 'Zip' col and that col is an (int)
    latlon = latlon[['Zip', 'Latitude', 'Longitude']]
    # clean only one col 'Net Earn-s'. Clean up must happen b4 graph call
    data_cleaned = sanitize.clean_price_col(sr_df, initial_net_earn_col)
    data_mapped = data_cleaned.rename(columns={"Buyer Zip Code": "Zip"}, errors="raise")
    # pandas remove everything after dash in zip code
    data_mapped['Zip'] = data_mapped['Zip'].str.split('-').str[0]
    # turn into int
    data_mapped['Zip'] = data_mapped['Zip'].astype(int)
    merged_inner = pd.merge(left=data_mapped, right=latlon, how='left', on='Zip')  # add lat,lon via 'Zip'

    my_geoseries = gpd.GeoDataFrame(
        merged_inner,
        geometry=gpd.points_from_xy(merged_inner.Longitude, merged_inner.Latitude), crs="EPSG:4326"
    )  # 4326 MUST!

    sr_graph1.geo_net_sales_density_destinations(meta, my_geoseries)  # must spell as 'initial_net_earn_col'

    data_mapped.rename({'Buyer State': 'STUSPS', initial_net_earn_col: 'Net_Earnings'}, axis=1, inplace=True)
    data_mapped['STUSPS'] = data_mapped['STUSPS'].str.upper()

    # https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html shape files
    states = gpd.read_file('data/cb_2020_us_state_500k/cb_2020_us_state_500k.shp')
    states = states.to_crs("EPSG:2163")
    # 2163 MAKES IT CURLY; GUAM IS ON THE LEFT. #  re-project usa_main to equal-area conic projection "EPSG:2163"
    # states = states.to_crs("EPSG:3395") #3395 THIS MAKES IT FLAT; GUAM IS FAR RIGHT, DON'T USE IT!
    data_mapped_drop = data_mapped.drop(['Department', 'Category','Subcategory','Brand','Color','Size','Bundle Order?','Offer Order','NWT', 'Order Price', 'Zip'], axis=1)
    data_mapped_drop_group = data_mapped_drop.groupby(["STUSPS"])["Net_Earnings"].sum().round(1).reset_index()
    merged_inner_w_geo = pd.merge(left=states, right=data_mapped_drop_group, how='left', on='STUSPS')

    newusa = merged_inner_w_geo[['STUSPS', 'Net_Earnings', 'geometry']]
    #  !!! the "Net_Earnings" col, must be the 2nd col when form newusa !!!
    # type(newusa) must be: geopandas.geodataframe.GeoDataFrame for plotting. & df must have ['Net_Earnings']
    assert isinstance(newusa, gpd.geodataframe.GeoDataFrame)
    df_for_html = newusa.copy()  # just in case the graph will have unpredicted changes to newusa
    sr_graph1.geo_net_sales_density(meta, newusa)  # col must spell as 'Net_Earnings'
    df1 = utils.sort_df(df_for_html, 'Net_Earnings')
    df1.rename(columns={'STUSPS': 'Buyer State', 'Net_Earnings': initial_net_earn_col}, inplace=True)
    df2 = df1[['Buyer State', initial_net_earn_col]]
    return utils.html_table(df2, meta, head=head, index=index, filename='vis_geo_netsales_density.html')


def main(meta, sr_df):
    """
    Control center: runs all funcs in this file

    :param meta: metadata
    :param sr_df: sales_report raw df
    :return: None, puts html tables (x.html) & graphs into output folder (y.png)
    """
    vis_department(sr_df, meta, head=5, sort_by_count=True, ascending=False, index=False)  # => .html table Dept
    vis_cat_subcat(sr_df, meta, cat=True, head=5, tail=5, ascending=False, index=False)  # => .html table Cat
    vis_cat_subcat(sr_df, meta, cat=False, head=5, tail=5, ascending=False, index=False)  # => .html Subcat
    vis_category_trees(sr_df, meta, head=5, ascending=False, index=False)  # => .html & .png & [TOP-5 CAT]
    # partying brands sales:
    min_date = datetime(2020, 1, 1)
    if min_date <= meta.sr_middle_date:  # this's for 2020 & later
        parties_csv = data.datafile_path('parties_2020_2ndhalfyear.csv')
    else:
        parties_csv = data.datafile_path('parties.csv')  # for 2019 ans earlier
    vis_partying_brands(parties_csv, meta, sr_df, freq="M", head=13, index=True)  # .html & .png
    vis_highest_net_brands(sr_df, meta, head=9, ascending=False, index=False)  # .html & .png, array of bestsellers
    vis_birthday_cake(meta, sr_df)  # .html & .png
    vis_total_fees_paid(meta, sr_df)  # .html & .png
    vis_net_sales_density(meta, sr_df)  # .html & .png


if __name__ == "__main__":
    sr_filename = 'test_files/sales_activity_report.csv'  # 01/01/2020 - 05/18/2020
    meta = read_file.Metadata.parse_report(sr_filename)  # tested
    df = read_file.load_df(sr_filename, meta)  # tested
    main(meta, df)
