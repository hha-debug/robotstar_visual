import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
 

def remove_vertical_stripes(img, notch_width=3, threshold_rel=0.1, exclusion_rel=0.02):
        """
        Remove vertical periodic stripes from a grayscale image using notch filtering.

        This implementation uses OpenCV's cv2.dft / cv2.idft for Fourier transforms.

        Inputs:
            img: 2D uint8 grayscale image
            notch_width: half-width of notch (in frequency bins) around detected peaks
            threshold_rel: relative threshold (fraction of max profile-FFT magnitude) to detect stripe frequencies
            exclusion_rel: relative fraction of width around DC to exclude from notch detection

        Returns:
            img_back: uint8 restored image
            fshift: shifted 2D complex array (numpy complex128) of original image spectrum
            magnitude: log-magnitude of fshift (for visualization)
        """
        if img.ndim != 2:
                raise ValueError("img must be a 2D grayscale image")

        rows, cols = img.shape

        # 1) Detect stripe frequencies by 1D FFT of column-wise mean profile (we can use numpy here)
        profile = img.mean(axis=0)
        fft_profile = np.fft.fft(profile)
        fft_profile_shift = np.fft.fftshift(fft_profile)
        mag_profile = np.abs(fft_profile_shift)

        center = cols // 2
        exclusion = int(max(1, cols * exclusion_rel))

        th = mag_profile.max() * float(threshold_rel)
        peak_indices = np.where((mag_profile > th) & (np.abs(np.arange(cols) - center) > exclusion))[0]

        # 2) Use OpenCV DFT to compute 2-channel complex spectrum
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
        # convert to numpy complex array for convenient shifting and masking
        complex_spec = dft[:, :, 0].astype(np.complex128) + 1j * dft[:, :, 1].astype(np.complex128)
        fshift = np.fft.fftshift(complex_spec)

        # magnitude for visualization
        magnitude = np.log1p(np.abs(fshift))

        # build mask (float) and apply notches at detected column frequencies
        mask = np.ones((rows, cols), dtype=np.float32)
        w = int(max(1, notch_width))
        for idx in peak_indices:
                l = max(0, idx - w)
                r = min(cols, idx + w + 1)
                mask[:, l:r] = 0.0

        # apply mask to complex spectrum (broadcast)
        fshift_filtered = fshift * mask

        # inverse shift and convert back to 2-channel float32 for cv2.idft
        f_ishift = np.fft.ifftshift(fshift_filtered)
        back_2ch = np.dstack([np.real(f_ishift).astype(np.float32), np.imag(f_ishift).astype(np.float32)])
        img_back = cv2.idft(back_2ch, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

        # normalize to uint8
        img_back = np.clip(img_back, 0, 255).astype(np.uint8)

        return img_back, fshift, magnitude


def save_spectrum(magnitude, out_path):
    # normalize for saving as uint8
    mag_norm = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    mag_u8 = mag_norm.astype(np.uint8)
    cv2.imwrite(out_path, mag_u8)


def main():
    # Interactive mode using built-in input() to get parameters (no sys/argparse)
    print("--- remove_stripes.py (interactive) ---")
    in_path = input("Enter input image path (full path), or empty to exit: ").strip()
    if not in_path:
        print("No input provided. Exiting.")
        return

    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")

    out_overwrite = True
    out_choice = input("Overwrite input file? [Y/n] (default Y): ").strip().lower()
    if out_choice == 'n':
        out_overwrite = False
        out_path = input("Enter output path to save restored image: ").strip()
        if not out_path:
            print("No output path provided. Exiting.")
            return
    else:
        out_path = in_path

    def get_float(prompt, default):
        v = input(f"{prompt} (default {default}): ").strip()
        return float(v) if v else default

    def get_int(prompt, default):
        v = input(f"{prompt} (default {default}): ").strip()
        return int(v) if v else default

    threshold = get_float("Relative threshold for detecting stripe frequencies", 0.1)
    width = get_int("Notch half-width in frequency bins", 3)
    exclusion = get_float("Exclusion fraction around DC (0-0.5)", 0.02)
    save_spec = input("Save spectrum image? [y/N]: ").strip().lower() == 'y'
    spec_path = None
    if save_spec:
        spec_path = input("Spectrum save path (leave empty for <input>_spectrum.png): ").strip()

    img = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Failed to read image or not a supported image format")

    restored, fshift, magnitude = remove_vertical_stripes(img, notch_width=width,
                                                          threshold_rel=threshold,
                                                          exclusion_rel=exclusion)

    cv2.imwrite(out_path, restored)
    print(f"Restored image saved to: {out_path}")

    if save_spec:
        if spec_path:
            sp_path = spec_path
        else:
            base, _ = os.path.splitext(out_path)
            sp_path = base + '_spectrum.png'
        save_spectrum(magnitude, sp_path)
        print(f"Spectrum image saved to: {sp_path}")

    # Display results using matplotlib
    try:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title('Restored')
        plt.imshow(restored, cmap='gray')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Log magnitude spectrum')
        plt.imshow(magnitude, cmap='gray')
        plt.axis('off')

        plt.tight_layout()
        plt.show()
    except Exception:
        # If display fails (headless), ignore
        pass


if __name__ == '__main__':
    main()
