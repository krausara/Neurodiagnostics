from analysis import *
import os
# 4.1 Public available data
data_folder = 'data/'
subject = 'S001'
run = 'R01'
file_path = data_folder + subject + '/' + subject + run + '.edf'

# Load raw data
raw = mne.io.read_raw_edf(file_path, preload=True)

# Remove trailing dots of sensors names to fit into montage schema
clean_channel_mapping = {ch: ch.replace('.', '').upper() for ch in raw.ch_names}
raw.rename_channels(clean_channel_mapping)
# Montage needed for topomap, 'standard_1005' because 10-10 electrode placement with 64 sensors was used
montage = mne.channels.make_standard_montage('standard_1005')
raw.set_montage(montage, match_case=False)

# Create directory to store plots
dir_path = 'plots/public' 
os.makedirs(dir_path, exist_ok=True)

# Plot raw data
plot_data(raw, n_channels=64, file_path=f'{dir_path}/{subject}_{run}_raw_plot.png')
# Filter and plot the raw data
filtered = filtering(raw, l_freq=0.5)
plot_data(filtered, n_channels=64, file_path=f'{dir_path}/{subject}_{run}_filtered_plot.png')
# rereference and plot the filtered data
reref = rereferencing(filtered)
plot_data(reref, n_channels=64, file_path=f'{dir_path}/{subject}_{run}_reref_plot.png')
# compute and plot the PSD for the rereferenced data
# fmax = 80 Hz sampling freq
# n_fft = 160 sampling rate of data is 160/s 
psd = compute_psd(reref, fmax=80, n_fft=160, file_path=f'{dir_path}/{subject}_{run}_psd_plot.png')
# Plot a topomap for the alpha band
topoalpha(psd, file_path=f'{dir_path}/{subject}_{run}_topoalpha_plot.png')
