import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--features',type=str,
                    help='Features to be process')
parser.add_argument('--csv_save_files_dir',type=str, default = './csv/',
                    help='Directory which contains the saved CSV files of individual features ')
parser.add_argument('--stations_data_dir', type=str, default='./stations_data/',
                    help = 'Directory to store the information of individual stations,as well as their lat,lon')
args = parser.parse_args()



if __name__ == "__main__":
    features = args.features.split()
    csv_dir = args.csv_save_files_dir
    stations_data_dir = args.stations_data_dir
    
    if not os.path.exists(stations_data_dir):
        os.mkdir(stations_data_dir)

    merged_df = pd.read_csv(csv_dir + 'merged.csv',index_col=False)

    # Save locattion file
    all_coordinates = merged_df.groupby(['lat','lon']).count().reset_index()[['lat','lon']]
    station_names = []
    for index, row in all_coordinates.iterrows():
        stat_name = "station_" + str(index + 1)
        station_names.append(stat_name)
    
    station_names = pd.Series(station_names,copy = False)
    all_coordinates['stat_name'] = station_names
    all_coordinates = all_coordinates[['stat_name', 'lat', 'lon']]
    all_coordinates.to_csv(stations_data_dir+ 'location.csv', index = False)

    # create station dfs
    for index, row in all_coordinates.iterrows():
        stat_name = station_names[index]
        lat, lon = row['lat'], row['lon']
        station_df = merged_df[merged_df['lat'] == lat][merged_df['lon'] == lon].reset_index()
        station_df = station_df.drop(columns = ['index','lat','lon'])
        station_df = station_df[features]

        station_path = stations_data_dir + stat_name + '.csv'
        station_df.to_csv(station_path, index=False)    
    
    print("Created data from separate stations")
