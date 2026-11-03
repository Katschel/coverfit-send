# CoverFit Send

A [Calibre](https://calibre-ebook.com) plugin that emails books to your Kindle with the **cover fitted to the full Kindle screen**.

Calibre's built-in "Email to" sends your EPUB as it is, so a cover with a different aspect ratio ends up with black or white bars on the Kindle. CoverFit Send fixes that: before sending, it resizes the cover to your Kindle's screen size, on a temporary copy of the book. Your library file and your library cover are never touched.

## Features

- **Fits the cover to your Kindle's screen** before the book is emailed
- **Never modifies your library**: only a temporary copy is changed
- **One-click toolbar button** with a menu to send to your default address or pick another address
- **Uses Calibre's own email setup**: addresses and mail server come from *Preferences > Sharing books by email*
- **Kindle model list**: choose your model instead of typing pixel sizes (or enter a custom size)
- **Two fit modes**: stretch (fills exactly, may distort) or crop (keeps proportions, trims the edges)

## Installation

1. Download `CoverFit_Send.zip` from the [latest release](../../releases/latest).
2. In Calibre open **Preferences > Advanced > Plugins > Load plugin from file** and select the zip.
3. Restart Calibre.
4. If the button doesn't appear on its own, add it under **Preferences > Toolbars & menus**: choose *The main toolbar*, select **CoverFit Send** on the left and click the right arrow.

## Usage

1. Make sure *Preferences > Sharing books by email* has your Kindle address and a working mail server.
2. Select one or more books that have an EPUB format.
3. Click the **CoverFit Send** button to send to your default address, or open its menu and choose **Email to...** to pick another address.

## Settings

| Setting | What it does |
| --- | --- |
| Fit the cover to the Kindle screen | Turns the cover fitting on or off. When off, books are sent unchanged. |
| Default recipient | The address used by the main button. |
| Kindle model | Your Kindle, grouped by model. The matching pixel size is shown below it. |
| Fit mode | **Stretch to fit** fills the screen exactly and may distort. **Crop to fit** keeps proportions and trims the edges. |

## Supported Kindle models

| Model | Screen (px) |
| --- | --- |
| Kindle Basic (2022-2026) | 1072 x 1448 |
| Kindle Basic (2019) | 600 x 800 |
| Kindle Paperwhite (2024-2026) | 1264 x 1680 |
| Kindle Paperwhite (2021, 11th gen) | 1236 x 1648 |
| Kindle Paperwhite (2015-2018) | 1072 x 1448 |
| Kindle Paperwhite (2012-2013) | 758 x 1024 |
| Kindle Colorsoft (2024-2026) | 1264 x 1680 |
| Kindle Oasis (2017-2019) | 1264 x 1680 |
| Kindle Oasis (2016) | 1072 x 1448 |
| Kindle Voyage (2014) | 1072 x 1448 |
| Kindle Scribe 11" (2025-2026) | 1980 x 2640 |
| Kindle Scribe (2022-2024) | 1860 x 2480 |

Some of the newest sizes are derived from the screen size and pixel density of earlier models rather than from a spec sheet. If a size is wrong for your device, choose **Other / custom size** in the settings and please [open an issue](../../issues) so it can be corrected.

## How it works

1. Reads the EPUB's package file (OPF) to find the cover image, for both EPUB 2 and EPUB 3 style covers.
2. Resizes it to your Kindle's screen size with Pillow, on a temporary copy of the book.
3. Hands the copy to Calibre's own email job, which sends it using your saved mail settings.
4. The temporary files are deleted when Calibre closes.

## Limitations

- Only **EPUB** files are sent. Books without an EPUB are skipped.
- If no cover can be found in an EPUB, the book is sent unchanged.
- Stretch mode distorts covers that don't have the screen's proportions. Use crop mode to avoid that.

## Building from source

Clone the repository and, with Calibre closed, run from the folder that contains `__init__.py`:

```
calibre-customize -b .
calibre-debug -g
```

The first command builds the plugin and installs it into Calibre. The second starts Calibre with a console so errors are visible.

## License

Released under the GNU General Public License v3.0. See [LICENSE](LICENSE).
