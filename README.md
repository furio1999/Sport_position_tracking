# Sport_position_tracking
A small application to track the athlete gesture and motion over time

**key sports**: running, taekwondo, cycling, triathlon

**Frameworks**: Mediapipe

**Features**: 
- angle tracking
- trajectory tracking
- AI-Trainer

<p float="center">
  <img src="application/videos/tkd_clip.gif" width="49%" />
  <img src="application/videos/run_clip.gif" width="49%" />
</p>

angle tracking:
<p float="center">
  <img src="plots/angle_plot_tkd.png" width="30%" />
</p>

MediaPipe number body mapping:
<p float="center">
  <img src="application/Photos/pose_tracking_full_body_landmarks.png" width="50%" />
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
python sport_pose.py --video [PATH_TO_VIDEO] #eg. --video videos/tkd.mp4
```

activate the desired features
```bash
#perform trajectory tracking (taekwondo video)
python sport_pose.py --trajectory_tracking

#perform running form evaluation (use 1500_doha.mp4 to reproduce my results)
python sport_pose.py --running_evaluation
```
choose the desired body part to track
```bash
python sport_pose.py --body_part [NAME_OF_PART]
#see the help section
```
choose a single mediapipe joint to track
```bash
python sport_pose.py --joint [NUMBER OF JOINT]
#refers to mediapipe number mapping https://google.github.io/mediapipe/solutions/pose.html
```

help and explanation on a specific command
```bash
python sport_pose.py [COMMAND] -help
#es. --body_part -help
```
