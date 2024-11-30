import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Simulation parameters
fs = 1e6  # Sampling frequency (1 MHz)
t = np.linspace(0, 1e-3, int(fs * 1e-3), endpoint=False)  # Time vector (1 ms duration)
f_center = 100e3  # Central frequency of the pulse (100 kHz)

# Medium parameters
humidity_levels = [0.1, 0.3, 0.5, 0.7, 0.9]  # Simulated humidity levels (fractional)

# Pulse generation
def generate_pulse(t, f_center):
    return np.sin(2 * np.pi * f_center * t) * np.exp(-5e3 * t)  # Damped sine wave

# Low-pass filter (Butterworth)
def butter_lowpass(cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    return lfilter(b, a, data)

# TDR function of transfer
def TDR_transfer_function(frequencies, humidity):
    R = 1 / (0.1 + 0.9 * humidity)  # Example resistance dependency on humidity
    C = (0.5 + 0.5 * humidity) * 1e-9  # Capacitance changes with humidity
    L = 1e-6  # Inductance fixed for simplicity
    G = 1e-3 * humidity  # Conductance changes with humidity
    gamma = np.sqrt((R + 1j * 2 * np.pi * frequencies * L) * (G + 1j * 2 * np.pi * frequencies * C))
    Z_soil = np.sqrt((R + 1j * 2 * np.pi * frequencies * L) / (G + 1j * 2 * np.pi * frequencies * C))
    return gamma, Z_soil

# S-parameter calculation
def calculate_s_parameters(frequencies, Z_soil, Z0=50):
    reflection_coefficient = (Z_soil - Z0) / (Z_soil + Z0)
    transmission_coefficient = 1 - np.abs(reflection_coefficient) ** 2  # Simplified
    return reflection_coefficient, transmission_coefficient

# Generate and process pulse
pulse = generate_pulse(t, f_center)
filtered_pulse = lowpass_filter(pulse, cutoff=150e3, fs=fs)

# FFT of the input signal
frequencies = np.fft.rfftfreq(len(t), d=1 / fs)
pulse_fft = np.fft.rfft(filtered_pulse)

# Loop over humidity levels
plt.figure(figsize=(10, 6))
for humidity in humidity_levels:
    gamma, Z_soil = TDR_transfer_function(frequencies, humidity)
    reflection, transmission = calculate_s_parameters(frequencies, Z_soil)
    # Modulate signal with transfer function
    output_fft = pulse_fft * np.exp(-gamma * 1)  # Assuming unit length probe
    output_signal = np.fft.irfft(output_fft)
    plt.plot(t[:len(output_signal)], output_signal, label=f'Humidity: {humidity:.1f}')

# Save TDR time-domain signal plot
plt.title("TDR Signal with Different Humidity Levels")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.savefig("DSP_S-Parameter_Simulation_Soil_Moisture\\tdr_signals_time_domain.png")
plt.show()

# S-parameters visualization
plt.figure(figsize=(10, 6))
for humidity in humidity_levels:
    gamma, Z_soil = TDR_transfer_function(frequencies, humidity)
    reflection, transmission = calculate_s_parameters(frequencies, Z_soil)
    plt.plot(frequencies, 20 * np.log10(np.abs(reflection)), label=f'Humidity: {humidity:.1f}')

# Save S11 parameter plot
plt.title("S11 Parameter (Reflection Coefficient) vs Frequency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.legend()
plt.grid()
plt.savefig("DSP_S-Parameter_Simulation_Soil_Moisture\\s11_reflection_coefficient.png")
plt.show()
