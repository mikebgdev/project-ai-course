## Things to Do
### AI
#### YOLO v8 or v9
- :white_check_mark: Detect people
- :white_check_mark: Track their movement

#### Computer Vision
- :white_check_mark: Timer for how long they stay in a specific location
- Emotion detection
- :white_check_mark: Pixelate faces
- Gender (Male or Female)

### Big Data
#### Objective

| uid | appears | disappears |
|-----|---------|------------|
| 12  | 5131321 | 12312412   |
| 123 | 1231451 | 12314123   |
| 122 | 1231412 | 13145123   |

- Average time: 50 min
- Busiest hour: 18:00

### Deployment / Presentation / ETC
- :white_check_mark: Developing a web interface with the model, better than running a .py locally
- :interrobang: Ability to use a web video feed

## Roadmap
### AI
1. :white_check_mark: Implement YOLO to detect people in video
2. :white_check_mark: Implement detection of time spent in scene (if possible)
3. :interrobang: Save previous data (Data processing at the end)
4. Simultaneously:
   - :white_check_mark: Pixelate faces
   - Emotion detection
   - :white_check_mark: Tracking
5. :white_check_mark: Implement the model in a web environment (Like dogs and cats)

### Big Data
1. Extract and save more video data
2. Continue brainstorming based on the "Drug smoking" section

#### Drug smoking (fictional)
- AI Data -> Redis -> Hadoop -> Database -> API
- Hadoop via API -> Insert rows into CSV -> PowerBI Visualization
- Ability to detect if the same person passes through the same location again


