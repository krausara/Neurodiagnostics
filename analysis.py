import os
import mne
from mne.preprocessing import ICA
import matplotlib.pyplot as plt

def plot_data(data, n_channels, file_path):
    fig = data.plot(duration=20, n_channels=n_channels, show=False, scalings='auto')
    fig.savefig(file_path)
    plt.close(fig)

def plot_10_secs(data, data_type, artifact_windows, output_dir):
    for name, start_time in artifact_windows.items():
        fig = data.plot(start=start_time, duration=10.0, n_channels=len(data.ch_names), show=False)
        fig.savefig(os.path.join(output_dir, f"{name}_{data_type}.png"))
        plt.close(fig)

def filtering(raw, l_freq):
    '''
    Applies high-pass, low-pass and notch filtering to raw EEG data
    '''
    # Copy raw to avoid overriding original data
    filtered = raw.copy()
    # 1: High-pass filter 0.5 Hz to remove slow drifts 
    # 2: Low-pass filter 40 Hz to remove highfreq noise and muscle artefacts
    filtered.filter(l_freq=l_freq, h_freq=40.0, fir_design='firwin', verbose=False)
    # 3: Notch filter at 50 Hz (Europe standard) to remove line noise
    filtered.notch_filter(freqs=50.0, fir_design='firwin', verbose=False)
    return filtered

def rereferencing(filtered):
    '''
    Re-referencing the filtered EEG data to the average reference
    '''
    # Copy raw to avoid overriding original data
    reref = filtered.copy()
    # projection=False, the average reference is directly applied to the data
    reref.set_eeg_reference(ref_channels='average', projection=False)
    return reref    

def compute_psd(data, fmax, n_fft, file_path, avg=True):
    '''
    Compute the Power Spectral Density using Welch's method
    plot the spectrum and mark the typical EEG frequency bands
    '''
    # Welch's method for continous EEG data -> noise reduction, stationarity, FFT length
    psd = data.compute_psd(method="welch", fmin=0.5, fmax=fmax, n_fft=n_fft)
    fig = psd.plot(picks='eeg', average=avg, amplitude=False, show=False)

    ax = fig.axes[0]

    # Define frequence band ranges
    bands = {
        'Delta': (0.5, 4, '#9999ff'),
        'Theta': (4, 8, '#99ff99'),
        'Alpha': (8, 13, '#ffff99'),
        'Beta':  (13, 30, '#ffcc99'),
        'Gamma': (30, fmax, '#ff9999')
    }
    # Get y coordinate for band text position
    ymin, ymax = ax.get_ylim()
    text_y_position = ymax - (ymax - ymin) * 0.1  

    for band_name, (fmin, fmax, color) in bands.items():
        # Highlight the background area of the band
        ax.axvspan(fmin, fmax, color=color, alpha=0.3, zorder=0)
        
        # Add a text label centered horizontally within the band
        band_center = fmin + (fmax - fmin) / 2
        ax.text(band_center, text_y_position, band_name, 
                horizontalalignment='center', fontsize=10, 
                weight='bold', bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2'))

    ax.set_title("EEG Power Spectral Density (PSD) with Frequency Bands")
    fig.savefig(file_path)
    plt.close(fig)
    return psd

def topoalpha(data, file_path):
    '''
    Plots the alpha band's spatial distribution as a topographic map
    '''
    bounds = (8, 13)
    fig = data.plot_topomap(bands={'Alpha': bounds}, ch_type='eeg', sensors=True)
    fig.suptitle(f"Alpha Band ({bounds[0]}-{bounds[1]} Hz) Spatial Topomap", 
                 fontsize=7, weight='bold')
    fig.savefig(file_path)
    plt.close(fig)


def applyica(data, output_dir, n_components=None,):
    '''
    Fits ICA on preprocessed EEG data, generates a comprehensive properties plot (Time, Topo, PSD) for every component
    saves the figures to disk
    '''
    os.makedirs(output_dir, exist_ok=True)

    ica = ICA(n_components=n_components, random_state=42)
    ica.fit(data)

    for i in range(ica.n_components_):
        # plot_properties creates a single consolidated figure containing:
        # 1. Topographic map of the component weight spatial distribution
        # 2. Power Spectral Density (PSD) of the component
        # 3. Time-domain epoch/continuous activity trace
        fig = ica.plot_properties(data, picks=i, show=False)[0]

        fig.savefig(f'{output_dir}/ica_component_{i}.png')
        plt.close(fig)
    
    # Pop up the overview scroll plots for quick structural exploration
    # Scrollable time-course of activations
    ica.plot_sources(data, block=False)
    # Combined grid of all topographic maps
    ica.plot_components()

    return ica

def remove_artefacts(data, ica, exclude, output_dir):
    '''
    Removes the given components (exclude) from the EEG data
    Plots both original and excluded data
    Replot ICA componets
    '''
    #exclude the componants which are artefacts
    ica.exclude = exclude
    reconst_data = data.copy()
    ica.apply(reconst_data)

    # compare original with excluded data
    fig = data.plot(n_channels=len(data.ch_names), show_scrollbars=False)
    fig.savefig(f'{output_dir}/data_original.png')
    plt.close(fig)
    fig = reconst_data.plot(n_channels=len(data.ch_names), show_scrollbars=False)
    fig.savefig(f'{output_dir}/data_excluded.png')
    plt.close(fig)

    # replot ICA on the excluded data
    for i in range(ica.n_components_):
        fig = ica.plot_properties(reconst_data, picks=i, show=False)[0]
        fig.savefig(f'{output_dir}/ica_component_{i}_new.png')
        plt.close(fig)

    return reconst_data