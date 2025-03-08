# AutoEq-py313

이 프로젝트는 [Jaakko Pasanen의 AutoEq](https://github.com/jaakkopasanen/AutoEq) 프로젝트를 **Python 3.13.2와 호환**되도록 수정한 버전입니다.

## 프로젝트 소개
AutoEq는 헤드폰을 자동으로 이퀄라이징하는 도구입니다.

**[autoeq.app](https://autoeq.app)** 에서 시작할 수 있습니다.

이 Python 3.13.2 호환 버전에서는 다음과 같은 기능을 제공합니다:
* 헤드폰 주파수 응답 작업 및 파라메트릭 이퀄라이저 최적화 라이브러리
* 최신 Python 버전(3.13.2)과의 호환성
* 다양한 소스([oratory1990](https://www.reddit.com/r/oratory1990/wiki/index/list_of_presets/),
[crinacle](https://crinacle.com),
[Innerfidelity](https://www.stereophile.com/content/innerfidelity-headphone-measurements),
[Rtings](https://www.rtings.com/headphones/1-5/graph), headphone.com)의 헤드폰 [측정 데이터](./measurements) 모음
* 다양한 헤드폰 주파수 응답 [타겟](./targets) 데이터
* [결과](./results)에 사전 계산된 이퀄라이저 설정

![Sennheiser HD 800](./results/oratory1990/over-ear/Sennheiser%20HD%20800/Sennheiser%20HD%20800.png)

*Sennheiser HD 800 이퀄라이제이션 결과 그래프*

## Python 3.13.2 호환성 개선 사항
이 프로젝트는 원본 AutoEq의 코드를 Python 3.13.2에서 작동하도록 다음과 같은 부분을 수정했습니다:

1. **rapidfuzz 라이브러리 호환성**: `manufacturer_index.py` 파일에서 `rapidfuzz.fuzz.ratio` 함수를 직접 임포트하여 사용하도록 수정
2. **PIL.Image 사용 개선**: `oratory1990_crawler.py`에서 `Image.open()`을 컨텍스트 매니저 패턴으로 사용하여 자동 파일 닫기 기능 추가
3. **PyPDF2 사용 개선**: PDF 파일 처리 시 더 안전한 읽기와 빈 PDF 파일/페이지에 대한 예외 처리 추가
4. **requests 라이브러리 호환성**: `hypethe_sonics_crawler.py`에서 `requests.get()` 호출에 헤더와 타임아웃 추가하여 안정성 향상

### Updates
**2023-10-29** AutoEq version 4.0.0. Improved and unified naming conventions across the project. Cleaned up obsolete
files and reorganized directory structure. Completely reworked database management tools.

**2022-05-14** Web application. Reorganized measurements and results.

**2022-10-30** Restructured the project and published in PyPi. Source code moved under [autoeq](./autoeq) directory and 
command line usage changed from `python autoeq.py` to `python -m autoeq` with underscores `_` replaced with hyphens `-`
in the parameter names. 

**2022-09-18** Parametric eq optimizer reworked. The new optimizer supports shelf filters, has a powerful configuration
system, run 10x faster, has limits for Fc, Q and gain value ranges and treats +10 kHz range as average value instead of
trying to fix it precisely.

## Usage
AutoEq produces settings for basically all types of equalizer apps but does not do the equalization itself. You'll need
a different app for that. Go to **[autoeq.app](https://autoeq.app)** and select your equalizer app of choice. Quick
instructions for importing the produced settings will be shown there.

## Command Line Use
In addition to the web application, AutoEq can be used from command line (terminal). This is advanced use mainly
intended for developers. The following instructions apply for command line and Python interface use.

### Installing
- Download and install Git: https://git-scm.com/downloads. When installing Git on Windows, use Windows SSL verification
instead of Open SSL or you might run into problems when installing project dependencies.
- Download and install 64-bit **[Python 3](https://www.python.org/getit/)**. Make sure to check *Add Python 3.X to PATH*.
- You may need to install [libsndfile](http://www.mega-nerd.com/libsndfile/) if you're having problems with `soundfile`
when installing and/or running AutoEq.
- On Linux you may need to install Python dev packages
```shell
sudo apt install python3-dev python3-pip python3-venv
```
- On Linux you may need to install [pip](https://pip.pypa.io/en/stable/installing/)
- On Windows you may need to install
[Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, and 2019](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
- Open a terminal / command prompt. On Windows, search `cmd` in the start menu.
- Clone AutoEq
```shell
git clone https://github.com/jaakkopasanen/AutoEq.git
```
- Go to AutoEq location
```shell
cd AutoEq
```
- Create a python virtual environment
```shell
python -m venv venv
```
- Activate virtualenv
```shell
# On Windows
venv\Scripts\activate.bat
# On Linux and Mac
. venv/bin/activate
```
- Update pip
```shell
python -m pip install -U pip
```
- Install required packages
```shell
python -m pip install -U -e .
```
- Verify installation. If everything went well, you'll see the list of command line parameters AutoEq accepts.
```shell
python -m autoeq --help
```

```shell
python -m autoeq --input-file="measurements/oratory1990/data/over-ear/Sennheiser HD 800.csv" --output-dir="my_results" --target="targets/harman_over-ear_2018_wo_bass.csv" --max-gain=24 --parametric-eq --parametric-eq-config=4_PEAKING_WITH_LOW_SHELF,4_PEAKING_WITH_HIGH_SHELF --bass-boost=6 --convolution-eq --fs=48000 --bit-depth=32 --f-res=16
```

When coming back at a later time you'll only need to activate virtual environment again
```shell
# On Windows
cd AutoEq
venv\Scripts\activate.bat
# On Linux and Mac
cd AutoEq
. venv/bin/activate
```

To learn more about virtual environments, read [Python' venv documentation](https://docs.python.org/3.9/library/venv.html).

#### Updating
AutoEq is in active development and gets new measurements, results and features all the time. You can get the latest
version from git
```shell
git pull
```

Dependencies may change from time to time, you can update to the latest with
```shell
python -m pip install -U -e .
```

#### Checking Installation
This prints out CLI parameters if installation was successful.
```shell
python -m autoeq --help
```

### Example
Equalizing Sennheiser HD 650 and saving results to `my_results/`:
```shell
python -m autoeq --input-file="measurements/oratory1990/data/over-ear/Sennheiser HD 650.csv" --output-dir="my_results" --target="targets/harman_over-ear_2018.csv" --convolution-eq --parametric-eq --ten-band-eq --fs=44100,48000
```

### Building
Add changelog entry before building and update version number in pyproject.toml!

Install `build` and `twine`
```shell
python -m pip install build twine
```

Add updates to `autoeq/README.md` before building!

Build PyPi package on Windows
```shell
copy /y README.md README.md.bak && copy /y autoeq\README.md README.md && python -m build && copy /y README.md.bak README.md && del README.md.bak
```

Build PyPi package on Linux / MacOS
```shell
cp README.md README.md.bak && cp autoeq/README.md README.md && python -m build && cp README.md.bak README.md && rm README.md.bak
```

publish
```shell
python -m twine upload dist/autoeq-<VERSION>*
```

Remember to add Git tag!

## Contact
[Issues](https://github.com/jaakkopasanen/AutoEq/issues) are the way to go if you are experiencing problems or have
ideas or feature requests. Issues are not the correct channel for headphone requests because this project sources the
measurements from other databases and a headphone missing from AutoEq means it has not been measured by any of the
supported sources.

You can find me in [Reddit](https://www.reddit.com/user/jaakkopasanen),
[Audio Science Review](https://www.audiosciencereview.com/forum/index.php?members/jaakkopasanen.17838/) and
[Head-fi](https://www.head-fi.org/members/jaakkopasanen.491235/) if you just want to say hello.

## 라이센스
이 프로젝트는 원본 AutoEq와 동일하게 MIT 라이센스를 따릅니다. 원본 저작권은 Jaakko Pasanen에게 있습니다.

```
MIT License

Copyright (c) 2018-2022 Jaakko Pasanen
Copyright (c) 2023 Python 3.13.2 호환 버전 제작자

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
