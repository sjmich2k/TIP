## *THE INTANGIBLE PERFORMANCE*
A python prototyping commission from *Marie Kang* for her masters graduation project.

**DISCLAIMER:** this is a prototype, so the code structure might not be very pretty or optimized.

### About the Project
The project aims to convert a usage of a mobile device to musically interpretative outputs.
The outputs contain machine output and an augmented musical score designed by Marie.

My job is to make an application (prototype) that can parse gestures out of a screen recording of a mobile device with its owner doing every day tasks.
From the parsed gestures, the application then can shoot out signals via usb cables to operate devices, 
and fill out the score, both real-time.


### How to Use
1. Clone repository and `cd` into repository root using command prompt (or your favorite IDE)
2. Create new virtual environment with `python -m venv venv`
3. Activate the virtual environment 
   - on Windows: `venv\Scripts\activate`
   - on macOS: `source venv/bin/activate`
4. Install dependencies using `pip install -r requirements.txt`
5. Run main.py using `python main.py`


### Libraries Used
- OpenCV: video parsing, pixel difference detection, optical flow calculation, etc.
- PyGame: playing sounds & constructing the 'Score'


### Work Duration
- Main Prototype: 2023 May - June
- Score Creation: 2023 Oct 5


### Work Distribution
- Idea, Design, Fabrication, Setup, Presentation: Marie Kang
- Programming: Sungjin Kim (Me)
- Sound Design: Johann W. Kim


### 