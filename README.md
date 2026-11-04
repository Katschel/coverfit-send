# CoverFit Send

A Calibre plugin that emails books to your e-reader with the cover fitted to the device's screen.

Some e-readers show a cover with borders or a different aspect ratio than the screen. CoverFit Send resizes the cover of a temporary copy of the EPUB to your device's screen size right before it is sent by email. Your library and the original file stay untouched.

## Features

- Resizes the cover to the exact screen size of your device (stretch) or fills it while keeping proportions (crop)
- Device list grouped by brand: Kindle, Kobo, Tolino, PocketBook, Onyx Boox, plus a custom size for any other e-reader
- Toolbar button with a menu to send directly to any address set up in Calibre
- Works on a temporary copy; the original EPUB and the library cover are never modified
- If no cover can be found, the book is sent unchanged and you get a notice

## Installation

1. Download `CoverFit_Send.zip`.
2. In Calibre: Preferences > Plugins > Load plugin from file, then pick the zip.
3. Restart Calibre.

## Setup

1. Set up your mail server and recipient addresses under Preferences > Sharing books by email.
2. Open the plugin settings (toolbar button menu > Settings...).
3. Choose your brand and model. If your device is not listed, choose "Other / custom size" and enter its screen resolution in pixels (portrait).
4. Choose the fit mode and the default recipient.

## Usage

Select one or more books and click the CoverFit Send button, or use its menu to pick another recipient. "Fit cover to screen" in the menu switches the cover adjustment on or off.

Only EPUB files are sent.

## Notes

- Screen sizes are portrait pixel resolutions. Models with the same screen are grouped into one entry. Please verify the value for your device.
- For color E Ink devices the listed resolution is that of the black-and-white layer.
- The Boox Picco is listed from announced specifications.
- Requires Calibre 5.0 or newer and Pillow (included with Calibre).
