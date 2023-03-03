import xarray as xr
import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--features',type=str,
                    help='Features to process')
parser.add_argument('--nc_files_dir',type=str, default = './data/nc_files/',
                    help='Directory of the .NC files of individual features')
parser.add_argument('--csv_save_files_dir',type=str, default = './data/csv/',
                    help='Directory to save the csv files, converted from the original .NC files ')

args = parser.parse_args()

if __name__ == "__main__":
    features = args.features.split()
    features = [feature.strip() for feature in features]
    print("Selected features", args.features)
    nc_dir = args.nc_files_dir
    csv_dir = args.csv_save_files_dir
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
        
    feature_dfs = {}
    for feature in features:
        print(nc_dir, feature)
        nc_file = nc_dir + feature + ".nc"
        print(nc_file)
        nc = xr.open_dataset(nc_file)
        csv_file = csv_dir + feature + '.csv'
        feature_df = nc.to_dataframe()
        feature_df.reset_index(inplace=True)

        # print(type(feature_df))
        feature_df.rename(columns= {feature_df.columns[-1]: feature}, inplace=True)
        feature_df = feature_df[['time','lat','lon',feature]]
        feature_dfs[feature] = feature_df
        feature_df.to_csv(csv_file)
        # print(feature, feature_dfs)
        print("Converted NC files of feature: {} to CSV".format(feature))

    merged_df = feature_dfs[features[0]]
    
    for feature in features[1:]:
        feature_df = feature_dfs[feature]
        merged_df = pd.merge(merged_df,feature_df, how = 'outer', on = ['time', 'lat', 'lon'] )
    
    merged_df.to_csv(csv_dir + 'merged.csv', index = False)


        # print(nc.to_dataframe())
        # nc.to_dataframe().to_csv('precip.csv')
