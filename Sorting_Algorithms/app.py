import time
import numpy as np
import scipy as sp
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class TrackedArray():
    def __init__(self, arr):
        self.array = np.copy(arr)
        self.reset()

    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []
        self.full_copies = []
    
    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.array[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.array))

    def getActivity(self, idx = None):
        if idx == None:
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])   

    def __getitem__(self, key):
        self.track(key, "get")
        return self.array.__getitem__(key)

    def __setitem__(self, key, value):
        self.array.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.array.__len__()

def freq_map(x, xmin = 0, xmax = 1000, fmin = 120, fmax = 1200):
    return np.interp(x, [xmin, xmax], [fmin, fmax])

def freq_sample(freq, dt=1./60., samplerate=44100, oversample=2):
    """Create a sample with a specific freqency {freq} for a specified
    time {dt}"""
    mid_samples = np.int(dt * samplerate)
    pad_samples = np.int((mid_samples*(oversample-1)/2))
    total_samples = mid_samples + 2*pad_samples

    y = np.sin(2 * np.pi * freq * np.linspace(0, dt, total_samples))
    y[:pad_samples] = y[:pad_samples] * np.linspace(0, 1, pad_samples)
    y[- pad_samples:] = y[len(y) - pad_samples:] * \
        np.linspace(1, 0, pad_samples)

    return y

plt.style.use('dark_background')  
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 16

N = 30
FPS = 60

F_SAMPLE = 44100
OVERSAMPLE = 2

arr = np.round(np.linspace(1, 1000, N))
np.random.seed(0)
np.random.shuffle(arr)

# fig, ax = plt.subplots()
# ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
# ax.set_xlim([0, N])
# ax.set(xlabel="Index", ylabel="Value")
# plt.title("Unsorted array")
# plt.show()
"""
#Insertion Sort
algorithm = "Insertion"

toc = time.time()
###########################################################################################################
i = 1
while i < len(arr):
    j = i
    while j > 0 and arr[j-1] > arr[j]:
        arr[j-1], arr[j] = arr[j], arr[j-1]
        j -= 1
    i += 1
###########################################################################################################
tic = time.time()
time_taken = tic - toc
print(f"---------- {algorithm} Sort ----------")

print(f"Array Sorted in {time_taken*1E3:.1f} ms")
    
fig, ax = plt.subplots()
ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
ax.set_xlim([0, N])
ax.set(xlabel="Index", ylabel="Value")
plt.title(f"Sorted array using {algorithm} sort")
plt.show()


arr = np.round(np.linspace(1, 1000, N))
np.random.seed(0)
np.random.shuffle(arr)

fig, ax = plt.subplots()
ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
ax.set_xlim([0, N])
ax.set(xlabel="Index", ylabel="Value")
plt.title("Unsorted array")
plt.show()
"""
arr = TrackedArray(arr)
#Quick Sort
algorithm = "Quick"
###########################################################################################################
def quicksort(A, lo, hi):
    if lo < hi:
        p = partition(A, lo, hi)
        quicksort(A, lo, p-1)
        quicksort(A, p+1, hi)

def partition(A, lo, hi):
    pivot = A[hi]
    i = lo
    for j in range(lo, hi):
        if A[j] < pivot:
            A[j], A[i] = A[i], A[j]
            i += 1
    A[i], A[hi] = A[hi], A[i]
    return i

###########################################################################################################

toc = time.time()
quicksort(arr, 0, len(arr)-1)
tic = time.time()
time_taken = tic - toc
print(f"---------- {algorithm} Sort ----------")
print(f"Array Sorted in {time_taken*1E3:.1f} ms")

wav_data = np.zeros(np.int(F_SAMPLE*len(arr.values)*1./FPS), dtype=np.float)
dN = np.int(F_SAMPLE * 1./FPS)  # how many samples is each chunk

for i, value in enumerate(arr.values):
    freq = freq_map(value)
    sample = freq_sample(freq, dt=1./FPS, samplerate=F_SAMPLE,
                         oversample=OVERSAMPLE)

    
    idx_0 = np.int((i+0.5)*dN - len(sample)/2)
    idx_1 = idx_0 + len(sample)

    try:
        wav_data[idx_0:idx_1] = wav_data[idx_0:idx_1] + sample
    except ValueError:
        print(f"Failed to generate {i:.0f}th index sample")


wav_data = (2**15*(wav_data/np.max(np.abs(wav_data)))).astype(np.int16)
sp.io.wavfile.write(f"{algorithm}_sound.wav", F_SAMPLE, wav_data)

fig, ax = plt.subplots()
container = ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
ax.set_xlim([0, N])
ax.set(xlabel="Index", ylabel="Value")
txt = ax.text(0, 1000, "")
# plt.title(f"Sorted array using {algorithm} sort")
# plt.show()


def update(frame):
    txt.set_text(f"Access = {frame} ")
    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("#1f77b4")

    (idx, op) = arr.getActivity(frame)
    if op == "get":
        container.patches[idx].set_color("magenta")
    else:
        container.patches[idx].set_color("red")

    #fig.savefig(f"frames/{algorithm}_frame{frame:05.0f}.png")
    return (*container,txt)


ani = FuncAnimation(fig, update, frames=range(len(arr.full_copies)),
                    blit=True, interval=1000./FPS, repeat=False)
plt.title(f"Sorted array using {algorithm} sort")
plt.show()