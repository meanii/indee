indee video engine
> A video engine that converts a video to HDR and SDR formats and packages them into MPEG-DASH format.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Download sample video](#download-sample-video)
- [Usage](#usage)
- [References](#references)

## Installation

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- [Bento4](https://www.bento4.com/downloads/)

Install the required packages using the following commands:
```bash
git clone https://github.com/meanii/indee.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install Bento4 using the following reference:
https://www.bento4.com/downloads/
> make sure you keep the bento source in the root directory of the project.

## Configuration
Update the `config.yaml` file with the following configurations:
```yaml
indee_video_engine:
  # keeping the version number, so we can further maintain
  # some of deprecations
  version: "v1"
  log:
    enable: true
    level: "INFO" # DEBUG, INFO, WARNING, ERROR, CRITICAL

  # engine related basic configs
  configs:
    # you can configure the storage engine,
    # as of now we only support sqlite
    db:
      enable: true
      service: "sqlite"
    # run the engine as a api server, by default
    # it is just cli
    server:
      enable: true
      port: 8001

      # enabling prometheus metrics, for the further
      # analytics, and mastrics
      metrics:
        enable: false
        port: 9090
        
  # cache related configs
  cache:
    # ( os.CWD, cache.dir ), cache dir, the main working dir
    # for all video processing
    dirname: "%WORDIR/output/%DATE/%TIMESTAMP/"
  
  # video processing related configs
  banto:
    banto_dir: "banto" # banto dir, where all the banto files are stored, should be in the root of the project
    fragment: 8000 # 8 seconds
```

## Download sample video
Download the sample video from the following link: [Sample Video](https://www.rmp-streaming.com/test/gos/sollevante/short-form/hdr/original/fastflix-2160p.mp4)

## Usage
```bash
python cli.py --input=<sample_video> 
```

expected files will be generated in the `output` directory.
```
output
└── 2024-08-12
    └── 1723415529
        ├── 1080p
        │   ├── 1080p_hdr.mp4
        │   └── 1080p_sdr.mp4
        ├── 360p
        │   ├── 360p_hdr.mp4
        │   └── 360p_sdr.mp4
        ├── 480p
        │   ├── 480p_hdr.mp4
        │   └── 480p_sdr.mp4
        ├── 720p
        │   ├── 720p_hdr.mp4
        │   └── 720p_sdr.mp4
        ├── dash
        │   ├── hdr
        │   │   ├── audio
        │   │   │   └── und
        │   │   │       └── mp4a.40.2
        │   │   │           ├── init.mp4
        │   │   │           └── seg-1.m4s
        │   │   ├── manifest-hdr.mpd
        │   │   └── video
        │   │       └── hev1
        │   │           ├── 1
        │   │           │   ├── init.mp4
        │   │           │   └── seg-1.m4s
        │   │           ├── 2
        │   │           │   ├── init.mp4
        │   │           │   └── seg-1.m4s
        │   │           ├── 3
        │   │           │   ├── init.mp4
        │   │           │   └── seg-1.m4s
        │   │           └── 4
        │   │               ├── init.mp4
        │   │               └── seg-1.m4s
        │   └── sdr
        │       ├── audio
        │       │   └── und
        │       │       └── mp4a.40.2
        │       │           ├── init.mp4
        │       │           └── seg-1.m4s
        │       ├── manifest-sdr.mpd
        │       └── video
        │           └── hev1
        │               ├── 1
        │               │   ├── init.mp4
        │               │   └── seg-1.m4s
        │               ├── 2
        │               │   ├── init.mp4
        │               │   └── seg-1.m4s
        │               ├── 3
        │               │   ├── init.mp4
        │               │   └── seg-1.m4s
        │               └── 4
        │                   ├── init.mp4
        │                   └── seg-1.m4s
        └── fragments
            ├── 1080p_hdr.mp4
            ├── 1080p_sdr.mp4
            ├── 360p_hdr.mp4
            ├── 360p_sdr.mp4
            ├── 480p_hdr.mp4
            ├── 480p_sdr.mp4
            ├── 720p_hdr.mp4
            └── 720p_sdr.mp4

29 directories, 38 files
```

## References
- https://www.radiantmediaplayer.com/blog/demystifying-hdr-video.html
- https://www.radiantmediaplayer.com/blog/how-to-tell-if-my-video-file-is-hdr.html
- https://ottverse.com/bento4-mp4dash-for-mpeg-dash-packaging/