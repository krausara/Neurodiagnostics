from analysis import *
import os

data_folder = 'data/own_data/'
conditions = ['eyes_open', 'eyes_closed'] 

# 4.2 Own clean resting-state data
for condition in conditions:
    file_path = data_folder + condition + '.nedf'

    # Load raw data
    raw = mne.io.read_raw_nedf(file_path, preload=True)
    # Montage needed for topomap, 'standard_1005'
    montage = mne.channels.make_standard_montage('standard_1005')
    raw.set_montage(montage, match_case=False)

    # Create directory to store plots
    dir_path = f'plots/{condition}' 
    os.makedirs(dir_path, exist_ok=True)
    
    n_channels = len(raw.ch_names)

    fig = raw.plot_sensors(kind='topomap', show_names=True)
    fig.savefig(f'{dir_path}/sensors.png')
    plt.close(fig)
    # Plot raw data
    plot_data(raw, n_channels=n_channels, file_path=f'{dir_path}/{condition}_raw_plot.png')
    # Filter and plot the raw data
    filtered = filtering(raw, l_freq=0.5)
    plot_data(filtered, n_channels=n_channels, file_path=f'{dir_path}/{condition}_filtered_plot.png')
    # rereference and plot the filtered data
    reref = rereferencing(filtered)
    plot_data(reref, n_channels=n_channels, file_path=f'{dir_path}/{condition}_reref_plot.png')
    # compute and plot the PSD for the rereferenced data
    # n_fft = 500 sampling rate of data is 500/s 
    psd = compute_psd(reref, fmax=45, n_fft=500, file_path=f'{dir_path}/{condition}_psd_plot.png')
    psd_avg = compute_psd(reref, fmax=45, n_fft=500, file_path=f'{dir_path}/{condition}_psd_single.png', avg=False)
    # Plot a topomap for the alpha band
    topoalpha(psd, file_path=f'{dir_path}/{condition}_topoalpha_plot.png')