# CoverFit Send

A Calibre plugin that emails EPUBs to your e-reader with the cover resized to fit the device screen.

## Features

* **Cover Resizing**: Fits covers to your screen size via stretch or crop.
* **Device Support**: Presets for Kindle, Kobo, Tolino, PocketBook, Onyx Boox, or custom dimensions.
* **Calibre Integration**: Send directly using recipient addresses configured in Calibre.
* **Non-Destructive**: Operates on temporary files - original EPUBs and covers remain untouched.

## Installation

1. Download `CoverFit_Send.zip` from Releases.
2. In Calibre: **Preferences** > **Plugins** > **Load plugin from file**.
3. Select the ZIP file and restart Calibre.

## Setup

1. Configure recipient emails in Calibre under **Preferences** > **Sharing books by email**.
2. Open plugin settings (**Toolbar button** > **Settings...**).
3. Select your device model, fit mode, and default recipient.

## Usage

Select one or more books and click **CoverFit Send** (or use the dropdown menu to choose another recipient).

*Note: Only EPUB files are supported.*

## Building from source

1. Clone the repository and navigate to the project root directory (where `__init__.py` is located).
2. Build and install the plugin:

```bash
calibre-customize -b .
```

3. Launch Calibre in debug mode to view console logs and errors:

```bash
calibre-debug -g
```