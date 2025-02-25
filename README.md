<div align="center">
<img src="./docs/images/icon.png" width="192" alt="App icon" />

# VCF Generator Lite

**Repositories:**
[![Gitee repository](https://img.shields.io/badge/Gitee-repository-C71D23?logo=gitee)][RepositoryOnGitee]
[![GitHub repository](https://img.shields.io/badge/GitHub-repository-0969da?logo=github)][RepositoryOnGithub]

**Platforms:**
[![Windows exe](https://img.shields.io/badge/Windows-exe-0078D4?logo=windows)][ReleaseOnGitee]
[![Python pyzw](https://img.shields.io/badge/Python-pyzw-3776AB?logo=python&logoColor=f5f5f5)][ReleaseOnGitee]

**Languages:**
[中文](./README.zh.md) |
**English** |
<small>More translations are welcome!</small>

_The application currently only supports the Chinese language._

</div>

VCF generator, input name and phone number to automatically generate VCF files for batch import into the address book.

[![License](https://img.shields.io/github/license/HelloTool/VCFGeneratorLiteForTkinter)](./LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.md)

## Screenshot

<img src="./docs/images/screenshots/Snipaste_2025-02-08_10-30-21.png" width="600" alt="Snipaste_2025-02-08_10-30-21.png" />

## Download

### Application Package Type Description

Choose the most suitable package format based on your usage scenario:

| Package Format | Execution Method               | Use Case                                |
| -------------- | ------------------------------ | --------------------------------------- |
| Installer      | Install and run                | Long-term use/Desktop shortcut required |
| Portable       | Extract and run (USB portable) | No installation/Temporary use           |
| ZipApp         | Directly run by double-click   | Quick launch/Cross-platform usage       |

### Compatibility Requirements

Different packages require specific environments. Select the appropriate package for your system:

| Package Format     | Core Dependencies      | Architecture          | Special Notes                      |
| ------------------ | ---------------------- | --------------------- | ---------------------------------- |
| Installer/Portable | Windows 7+ environment | x86_64                | Requires patch files for Windows 7 |
| ZipApp             | Python 3.13 + Tkinter  | Architecture-agnostic | -                                  |

### Download Sources

Get packages through these channels:

- [Gitee Releases][ReleaseOnGitee]
- [GitHub Releases][ReleaseOnGithub]

System-specific packages:

| OS          | Installer     | Portable Package         | ZipApp File               |
| ----------- | ------------- | ------------------------ | ------------------------- |
| Windows 7+  | `*_setup.exe` | `*_portable_windows.zip` | `vcf_generator_lite.pyzw` |
| Linux/macOS | Not supported | Not supported            | `vcf_generator_lite.pyzw` |

### Windows 7 Compatibility Patch

<details>
<summary>Patch instructions (Windows 7 ONLY)</summary>

1. **Download Python embed package** from [PythonWin7][PythonWin7RepositoryOnGithub]:
   - `python-3.13.2-embed-amd64.zip`
2. **Extract required DLLs**:
   - `python313.dll`
   - `api-ms-win-core-path-l1-1-0.dll`
3. **Apply patch**:
   1. Complete software installation
   2. Navigate to `_internal` folder in installation directory
   3. Replace existing files with the extracted DLLs

</details>

## Usage

1. Open the app.
2. Copy the name and phone number in the format of `Name PhoneNumber` on each line into the editing box below;
   ```text
   Hardy Buck	13445467890
   Alva Mackintosh	13554678907
   Hobart Baker	13645436748
   ```
3. Click "生成" (Generate), select a path to save the file.
4. Copy the generated VCF file to your phone, select "Contacts" when opening the file, and then follow the prompts.
5. Wait for the import to complete.

> [!NOTE]
>
> - Tabs will be automatically converted to spaces for processing.
> - The program will automatically remove excess spaces from the input box.
> - If there are multiple spaces in each line, all characters before the last space will be treated as names.
>
> For example, ` Hardy Buck   13333333333   ` will be recognized as
>
> ```text
> Name: Hardy Buck
> Phone: 13333333333
> ```

## License

This project is open source under the [MIT license](./LICENSE)

- [Fluent Emoji](https://github.com/microsoft/fluentui-emoji)(used as application icon): MIT license
- [Python](https://www.python.org/): [Python license](https://docs.python.org/3/license.html)
- [UPX](https://upx.github.io/)(for compressing code): GPL-2.0 license
- [PyInstaller](https://pyinstaller.org/en/stable/)(for packaging as an APP): [GPL-2.0 license](https://pyinstaller.org/en/stable/license.html)
- [tkhtmlview](https://github.com/bauripalash/tkhtmlview): MIT License

## Development & Contribution

Please refer to the [Development Guide](./docs/dev/README.md) and the [Contribution Guide](./CONTRIBUTING.zh.md).

[RepositoryOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/
[RepositoryOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/
[ReleaseOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
[ReleaseOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
[PythonWin7RepositoryOnGithub]: https://github.com/adang1345/PythonWin7
