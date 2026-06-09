import os
from analysis import *

data_folder = 'own_data/'
condition = '20260529133138_artifacts'
protocol = 'eyes_open'

# 4.3 Own noisy data
file_path = data_folder + '_'.join([condition, protocol]) + '.nedf'

# Load raw data
raw = mne.io.read_raw_nedf(file_path, preload=True)
# Montage needed for topomap, 'standard_1005'
montage = mne.channels.make_standard_montage('standard_1005')
raw.set_montage(montage, match_case=False)
_, condition = condition.split('_', maxsplit=1)

n_channels = len(raw.ch_names)
# Create directory to store plots
dir_path = f'plots/{condition}' 
os.makedirs(dir_path, exist_ok=True)


# Extract events from the stim channel dynamically
events = mne.find_events(raw, stim_channel='STI 014', min_duration=0.002, verbose=False)
sfreq = raw.info['sfreq']

# Map the Event IDs to midpoints of 10-second windows
# Event pairs: (1,2)=Blinks, (3,4)=Lateral, (5,6)=Chew, (7,8)=Pz Noise
artifact_windows = {
    "eye_blink": events[events[:, 2] == 1][0][0] / sfreq + 2.0,            # 2.83s + 2s buffer
    "lateral_eye_movement": events[events[:, 2] == 3][0][0] / sfreq + 5.0, # 29.52s + 5s buffer
    "chewing": events[events[:, 2] == 5][0][0] / sfreq + 5.0,              # 60.05s + 5s buffer
    "channel_noise": events[events[:, 2] == 7][0][0] / sfreq + 5.0,        # 89.66s + 5s buffer
}

for name, start_time in artifact_windows.items():
    print(f"Saving 10s raw snippet for '{name}' starting at {start_time:.2f}s")
    fig = raw.plot(start=start_time, duration=10.0, n_channels=len(raw.ch_names), scalings='auto', title=f"Raw Snippet: {name}", show=False)
    fig.savefig(os.path.join(dir_path, f"432_raw_{name}.png"), dpi=300)
    plt.close(fig)

# Plot raw data
#plot_data(raw,n_channels=n_channels, file_path=f'{dir_path}/{condition}_raw_plot.png')

filtered = filtering(raw, l_freq=1.0)
reref = rereferencing(filtered)
applyica(raw, reref)