import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd

SENSOR_COLUMNS = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6',
       'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11',
       'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_16',
       'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21']

### All fleet engine at a time
def plot_all_units_per_dataset(df, columns = SENSOR_COLUMNS):
    datasets = df['dataset'].unique()
    fig, ax = plt.subplots(21, 4, figsize=(26, 70))
    for i, dataset_name in enumerate(datasets):
        dataset_df = df[df['dataset'] == dataset_name]
        for j, sensor in enumerate(columns):
            dataset_df.pivot(index='time_cycles', columns='unit', values=sensor) \
                .plot(ax=ax[j, i], legend=None, alpha=0.5)
            ax[j, i].set_title('{} - {}, across all units'.format(dataset_name, sensor))
            ax[j, i].grid(color='grey', linewidth=0.3)
    fig.tight_layout()
    plt.show()

### Plot for single fleet engine at at time
def plot_all_units(df, dataset_name, columns=SENSOR_COLUMNS):
    dataset_df = df[df['dataset'] == dataset_name]
    for sensor in columns:
        fig, ax = plt.subplots(figsize=(16, 8))
        dataset_df.pivot(index='time_cycles', columns='unit', values=sensor) \
            .plot(ax=ax, legend=None, alpha=0.5)
        ax.set_title('{} - {}, across all units'.format(dataset_name, sensor))
        ax.grid(color='grey', linewidth=0.3)
        plt.show()

### Plot unit and sensors
def plot_unit_sensors_ts(unit, df, features=SENSOR_COLUMNS, dataset_name='train_FD001', per_sensor=False):
    unit_df = df[(df['unit'] == unit) & (df['dataset'] == dataset_name)]
    unit_df.index = unit_df['time_cycles']
    unit_df = unit_df[features]

    scaler = StandardScaler()
    unit_sensor_sc = pd.DataFrame(scaler.fit_transform(unit_df), 
                                  columns=features)

    fig, ax = plt.subplots(figsize=(14, 6))
    unit_sensor_sc.plot(ax=ax)
    ax.grid(color='grey', linewidth=0.3)
    ax.set_title('{}, Unit: {} (scaled sensor measurements)'.format(dataset_name, unit), loc='left')
    plt.show()

    if per_sensor:
        for sensor in features:
            fig, ax = plt.subplots(figsize=(16, 6))
            unit_df[sensor].plot(ax=ax, label=sensor)
            ax.legend()
            ax.grid(color='grey', linewidth=0.3)
            ax.set_title('{}, Unit: {}'.format(dataset_name, unit), loc='left')
            plt.show()
            
            
### plot sensors for unit
def plot_sensors_for_unit_ts(unit_df, unit, features=SENSOR_COLUMNS, dataset_name='FD001', per_sensor=False):
#     unit_df = df[(df['unit'] == unit) & (df['dataset'] == dataset_name)]
    unit_df.index = unit_df['time_cycles']
    unit_df = unit_df[features]

    scaler = StandardScaler()
    unit_sensor_sc = pd.DataFrame(scaler.fit_transform(unit_df), 
                                  columns=features)

    fig, ax = plt.subplots(figsize=(14, 6))
    unit_sensor_sc.plot(ax=ax)
    ax.grid(color='grey', linewidth=0.3)
    ax.set_title('{}, Unit: {} (scaled sensor measurements)'.format(dataset_name, unit), loc='left')
    plt.show()

    if per_sensor:
        for sensor in features:
            fig, ax = plt.subplots(figsize=(16, 6))
            unit_df[sensor].plot(ax=ax, label=sensor)
            ax.legend()
            ax.grid(color='grey', linewidth=0.3)
            ax.set_title('{}, Unit: {}'.format(dataset_name, unit), loc='left')
            plt.show()
