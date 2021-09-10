# Sport_position_tracking
A small application to track the athlete gesture and motion over time

**key sports**: running, taekwondo, cycling, triathlon

**Frameworks**: Mediapipe


<p float="center">
  <img src="application/videos/tkdpose.mp4" width="49%" />
  <img src="application/videos/runpose.mp4" width="49%" />
</p>

Clone the repo:
```bash
git clone https://github.com/furio1999/Sport_position_tracking.git
```

```bash
cd application
```
start the video application:
```bash
# Run on the webcam
python sport_pose.py --camera

# Run on video 
python sport_pose.py --video [NAME_OF_VIDEO]
```

activate the desired features
```bash
#perform trajectory tracking
python sport_pose.py --trajectory_tracking
```
