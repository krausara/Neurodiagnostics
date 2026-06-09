import os
from analysis import *

data_folder = 'own_data/'
condition = '20260529133138_artifacts'
protocol = 'eyes_open'

# 4.3 Own noisy data
file_path = data_folder + '_'.join([condition, protocol]) + '.nedf'

# Create directory to store plots
_, condition = condition.split('_', maxsplit=1)
dir_path = f'plots/{condition}' 
os.makedirs(dir_path, exist_ok=True)

# Load raw data
raw = mne.io.read_raw_nedf(file_path, preload=True)
# Montage needed for topomap, 'standard_1005'
montage = mne.channels.make_standard_montage('standard_1005')
raw.set_montage(montage, match_case=False)

n_channels = len(raw.ch_names)

# Extract events from the stim channel dynamically
events = mne.find_events(raw, stim_channel='STI 014', min_duration=0.002, verbose=False)
sfreq = raw.info['sfreq']

# Map the Event IDs to midpoints of 10-second windows
# Event pairs: (1,2)=Blinks, (3,4)=Lateral, (5,6)=Chew, (7,8)=Pz Noise
artifact_windows = {
    "eye_blink": events[events[:, 2] == 1][0][0] / sfreq, #+ 2.0,             2.83s + 2s buffer
    "lateral_eye_movement": events[events[:, 2] == 3][0][0] / sfreq, # + 5.0,  29.52s + 5s buffer
    "chewing": events[events[:, 2] == 5][0][0] / sfreq, # + 5.0,              # 60.05s + 5s buffer
    "channel_noise": events[events[:, 2] == 7][0][0] / sfreq, # + 5.0,        # 89.66s + 5s buffer
}

# Plot each 10 second event
plot_10_secs(raw, data_type='raw', artifact_windows=artifact_windows, output_dir=dir_path)

# Preprocess EEG data
filtered = filtering(raw, l_freq=1.0)
reref = rereferencing(filtered)

# Apply ICA
output_dir = dir_path + '/ica_components_plots'
ica = applyica(reref, output_dir=output_dir)
# Based on ICA findings remove artefacts here Components 0, 1 and 9 were identified as such
cleaned_data = remove_artefacts(reref, ica=ica, exclude=[0, 1, 9], output_dir=output_dir)

# Replot each 10 second event
plot_10_secs(cleaned_data, data_type='cleaned', artifact_windows=artifact_windows, output_dir=dir_path)